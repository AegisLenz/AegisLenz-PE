from datetime import datetime, timedelta, timezone
from elasticsearch import Elasticsearch, exceptions as es_exceptions
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import json
import time
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI
from function import prompt_files, load_prompt, print_response, text_response, save_history

# .env 파일 로드
load_dotenv(override=True)

api_key = os.getenv("OPEN_AI_SECRET_KEY")
client = OpenAI(api_key=api_key)
encoder = tiktoken.encoding_for_model("gpt-4-mini")

def save_logs_to_file(logs, filename):
    """
    로그를 JSON 파일로 저장합니다.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)
        print(f"로그가 파일에 저장되었습니다: {filename}")
    except Exception as e:
        print(f"로그 저장 중 오류 발생: {str(e)}")

def initialize_elasticsearch():
    """Initialize Elasticsearch client."""
    es_host = os.getenv("ES_HOST")
    es_port = os.getenv("ES_PORT")

    if not es_host or not es_port:
        raise ValueError("ES_HOST and ES_PORT must be set in .env file.")

    return Elasticsearch(f"{es_host}:{es_port}", max_retries=10, retry_on_timeout=True, request_timeout=120)

def fetch_attack_logs():
    """
    "cloudtrail-attack-logs" 인덱스에서 하루 동안 발생한 모든 공격 로그를 가져옵니다.
    전날 공격이 없어서 이전 공격을 가져옵니다.
    """
    es = initialize_elasticsearch()

    # 현재 날짜만 가져오기 (시간 제거)
    now = datetime.now(timezone.utc).date()
    # 올바른 날짜 범위 계산
    past_day = now - timedelta(days=17)
    past2_day = now - timedelta(days=16)

    query = {
        "query": {
            "range": {
                "@timestamp": {
                    "gte": past_day.isoformat(),
                    "lte": past2_day.isoformat(),
                    "format": "strict_date_optional_time"
                }
            }
        },
        "sort": [{"@timestamp": {"order": "asc"}}],
        "size": 1000
    }

    try:
        print("cloudtrail-attack-logs 인덱스에서 로그를 가져옵니다...")
        print(f"쿼리 조건 확인: {json.dumps(query, indent=2)}")

        response = es.search(index="cloudtrail-attack-logs", body=query, scroll="1m")
        scroll_id = response["_scroll_id"]
        logs = [hit["_source"] for hit in response["hits"]["hits"]]

        print(f"첫 번째 검색 결과 개수: {len(response['hits']['hits'])}")

        while True:
            scroll_response = es.scroll(scroll_id=scroll_id, scroll="1m")
            hits = scroll_response["hits"]["hits"]
            if not hits:
                break
            logs.extend([hit["_source"] for hit in hits])  # 새로 가져온 데이터를 병합
            print(f"현재까지 가져온 로그 개수: {len(logs)}")

        print(f"총 {len(logs)}개의 공격 로그를 가져왔습니다.")
        save_logs_to_file(logs, "attack_logs.json")
        return logs

    except es_exceptions.ConnectionError as e:
        print(f"Elasticsearch 연결 오류: {str(e)}")
        return []
    except es_exceptions.RequestError as e:
        print(f"Elasticsearch 요청 오류: {str(e)}")
        return []
    except Exception as e:
        print(f"Elasticsearch에서 로그를 가져오는 중 오류 발생: {str(e)}")

    return []


# 공격 10초 전,후 로그 가져오기
def fetch_logs_for_attack(es, log):
    timestamp = log.get("@timestamp")
    if not timestamp:
        return []

    log_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    start_time = (log_time - timedelta(seconds=10)).isoformat()
    end_time = (log_time + timedelta(seconds=10)).isoformat()
    index_name = f"cloudtrail-logs-{log_time.strftime('%Y.%m.%d')}"

    query = {
        "query": {
            "range": {
                "@timestamp": {
                    "gte": start_time,
                    "lte": end_time,
                    "format": "strict_date_optional_time"
                }
            }
        },
        "size": 1000
    }

    try:
        response = es.search(index=index_name, body=query)
        return [hit["_source"] for hit in response["hits"]["hits"]] 
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return []

def process_logs_by_token_limit(logs, token_limit=120000):
    """
    로그 데이터를 토큰 한계를 고려해 나눕니다.
    """
    processed_chunks, current_chunk, current_token_count = [], [], 0

    for log in logs:
        log_string = json.dumps(log)
        log_token_count = len(encoder.encode(log_string))

        if current_token_count + log_token_count > token_limit:
            print(f"청크 생성: 현재 청크 토큰 수 {current_token_count}, JSON 개수 {len(current_chunk)}")

            processed_chunks.append(current_chunk)
            current_chunk, current_token_count = [], 0

        current_chunk.append(log)
        current_token_count += log_token_count

    if current_chunk:
        print(f"청크 생성: 현재 청크 토큰 수 {current_token_count}, JSON 개수 {len(current_chunk)}")
        processed_chunks.append(current_chunk)

    return processed_chunks

def summarize_logs(log_chunks):
    """
    각 로그 청크를 요약하고 요약 결과를 반환합니다.
    """
    template_content = load_prompt(prompt_files["daily"])
    response_list = []

    for index, chunk in enumerate(log_chunks, start=1):
        log_string = "\n".join(json.dumps(log) for log in chunk)
        formatted_prompt = template_content.format(logs=log_string)

        prompt_txt = {"daily": {"role": "system", "content": formatted_prompt}}

        try:
            response = text_response(client, "gpt-4o-mini", [prompt_txt["daily"]])
            if response:
                response_list.append(response)
                print(f"Chunk {index} 처리 완료. 응답 추가됨.")
                print_response(f"Chunk {index} 요약", response)
                save_history([{"role": "chunk", "content": response}], "chunk_all.txt", append=True)
            else:
                print(f"Chunk {index} 처리 중 응답이 비어 있습니다.")
        except Exception as e:
            print(f"Chunk {index} 처리 중 오류 발생: {str(e)}")

    return response_list  # 처리된 요약을 반환


def is_duplicate_log(log, seen_logs):
    """필드 비교하여 중복 제외"""
    log_key = (
        log.get("@timestamp"),
        log.get("eventName"),
        log.get("eventID")
    )
    if log_key in seen_logs:
        return True
    seen_logs.add(log_key)
    return False


def fetch_related_logs_and_summarize(attack_logs):

    """
    여러 공격 로그의 타임스탬프를 기반으로 관련 로그를 가져오고 요약합니다.
    중복 로그는 해시값을 기준으로 제거됩니다.
    """
    es = initialize_elasticsearch()
    seen_logs = set()
    deleted_logs = []

    # 공격 로그를 중복 방지를 위해 seen_logs에 추가
    for log in attack_logs:
        log_key = (
            log.get("@timestamp"),
            log.get("eventName"),
            log.get("eventID")
        )
        seen_logs.add(log_key)


    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_log = {executor.submit(fetch_logs_for_attack, es, log): log for log in attack_logs}
        related_logs_summaries = []
        all_related_logs = []  # 모든 관련 로그를 누적 저장

        for attack_log, future in zip(attack_logs, as_completed(future_to_log)):
            related_logs = future.result()

            print(f"가져온 관련 로그 개수 : {len(related_logs)}")

            if not related_logs:
                continue

            unique_logs = []
            for log in related_logs:
                if is_duplicate_log(log, seen_logs):
                    deleted_logs.append(log)
                else:
                    unique_logs.append(log)

            print(f"삭제된 로그 개수: {len(deleted_logs)}")
            print(f"가져온 관련 로그 개수 (중복 및 공격 로그 제외 후): {len(unique_logs)}")

            all_related_logs.extend(unique_logs)
            log_chunks = process_logs_by_token_limit(unique_logs)
            timestamp = attack_log.get("@timestamp")
            chunk_summaries = summarize_logs(log_chunks)  or []  # None이면 빈 리스트로 대체
            related_logs_summaries.extend(chunk_summaries)

    # 모든 관련 로그를 한 번에 저장
    save_logs_to_file(all_related_logs, "related_logs.json")

    # 전체 관련 로그 요약
    combined_summary = "\n".join(related_logs_summaries)
    final_prompt = combined_summary + f"\n데이터의 관계와 흐름을 파악해서 요약하세요. 반드시 제목은 **{timestamp}에 발생한 공격의 전후로그 분석**이라고 해야합니다."

    try:
        final_summary = text_response(client, "gpt-4o-mini", [{"role": "user", "content": final_prompt}])
        save_history([{"role": "summary", "content": final_summary}], "final_summary.txt", append=True)
        print("최종 요약 완료.")
        return final_summary
    except Exception as e:
        print(f"최종 요약 생성 중 오류 발생: {str(e)}")
        return None

def extract_cloudTrail():
    """
    전체 로그 처리 및 요약.
    """
    attack_logs = fetch_attack_logs()

    if not attack_logs:
        print("가져온 공격 로그가 없습니다. 작업을 종료합니다.")
        return

    final_summary = fetch_related_logs_and_summarize(attack_logs)

    if final_summary:
        print("최종 요약:")
        print(final_summary)


if __name__ == "__main__":
    start_time = time.time()
    print("CloudTrail 로그 요약을 시작합니다...")
    extract_cloudTrail()

    print(f"실행 시간: {time.time() - start_time :.2f}초")
