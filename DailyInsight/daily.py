from datetime import datetime, timedelta, timezone
from elasticsearch import Elasticsearch, exceptions as es_exceptions
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
encoder = tiktoken.encoding_for_model("gpt-4")

def fetch_all_logs_with_scroll():
    """
    Elasticsearch에서 Scroll API를 사용해 로그를 가져옵니다.
    """
    es_host = os.getenv("ES_HOST")
    es_port = os.getenv("ES_PORT")

    if not es_host or not es_port:
        raise ValueError("ES_HOST와 ES_PORT가 .env 파일에 설정되어 있지 않습니다.")

    es = Elasticsearch(f"{es_host}:{es_port}", max_retries=10, retry_on_timeout=True, request_timeout=120)

    now = datetime.now(timezone.utc)  # 현재 시간
    past_days = now - timedelta(days=1)  # 1일 전 시간

    # Scroll API 설정
    query = {
        "query": {
            "range": {
                "@timestamp": {
                    "gte": past_days.isoformat(),
                    "lte": now.isoformat(),
                    "format": "strict_date_optional_time"
                }
            }
        },
        "sort": [{"@timestamp": {"order": "asc"}}],
        "size": 1000  # 한 번에 가져올 문서 수
    }

    try:
        print("Elasticsearch Scroll API를 사용해 로그를 가져옵니다...")

        # Scroll 시작
        response = es.search(index="cloudtrail-logs-*", body=query, scroll="1m")
        scroll_id = response["_scroll_id"]
        logs = [hit["_source"] for hit in response["hits"]["hits"]]

        while True:
            # Scroll 계속해서 가져오기
            scroll_response = es.scroll(scroll_id=scroll_id, scroll="1m")
            hits = scroll_response["hits"]["hits"]
            if not hits:
                break

            logs.extend([hit["_source"] for hit in hits])

        print(f"총 {len(logs)}개의 로그를 Elasticsearch에서 가져왔습니다.")
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

def calculate_token_count(logs):
    """
    로그 데이터의 총 토큰 수를 계산합니다.
    """
    log_string = "\n".join(json.dumps(log) for log in logs)
    return len(encoder.encode(log_string))

def process_logs_by_token_limit(logs, token_limit=120000):
    """
    로그 데이터를 토큰 한계를 고려해 나눕니다.
    """
    processed_chunks = []
    current_chunk = []
    current_token_count = 0

    for log in logs:
        log_string = json.dumps(log)
        log_token_count = len(encoder.encode(log_string))

        if current_token_count + log_token_count > token_limit:
            print(f"청크 생성: 현재 청크 토큰 수 {current_token_count}, JSON 개수 {len(current_chunk)}")

            processed_chunks.append(current_chunk)
            current_chunk = []
            current_token_count = 0

        current_chunk.append(log)
        current_token_count += log_token_count

    if current_chunk:
        print(f"청크 생성: 현재 청크 토큰 수 {current_token_count}, JSON 개수 {len(current_chunk)}")
        processed_chunks.append(current_chunk)

    return processed_chunks

def summarize_logs(log_chunks):
    """
    각 로그 청크를 요약하고 최종 요약을 생성합니다.
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

    if response_list:
        try:
            combined_prompt = "\n".join(response_list) + "\n데이터의 관계와 흐름을 파악해서 요약하세요."
            final_summary = text_response(client, "gpt-4o-mini", [{"role": "user", "content": combined_prompt}])
            print_response("최종 요약", final_summary)
            save_history([{"role": "summary", "content": final_summary}], "final_summary.txt", append=True)
        except Exception as e:
            print(f"최종 요약 생성 중 오류 발생: {str(e)}")

def extract_cloudTrail():
    """
    전체 로그 처리 및 요약.
    """
    logs = fetch_all_logs_with_scroll()

    if not logs:
        print("가져온 로그가 없습니다. 작업을 종료합니다.")
        return
    # 전체 JSON 로그 개수 출력
    print(f"가져온 전체 JSON 로그 개수: {len(logs)}")
    
    log_chunks = process_logs_by_token_limit(logs, token_limit=120000)
    print(f"토큰 한계를 기준으로 총 {len(log_chunks)}개의 청크로 나누어졌습니다.")

    # 각 청크의 JSON 개수 출력
    for idx, chunk in enumerate(log_chunks, start=1):
        print(f"Chunk {idx}의 JSON 개수: {len(chunk)}")

    summarize_logs(log_chunks)

if __name__ == "__main__":
    start_time = time.time()
    extract_cloudTrail()
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"실행 시간: {elapsed_time:.2f}초")
