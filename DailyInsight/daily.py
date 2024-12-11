from datetime import datetime, timedelta, timezone
from elasticsearch import Elasticsearch, exceptions as es_exceptions
import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI
from function import prompt_files, load_prompt, print_response, text_response, save_history

# .env 파일 로드
load_dotenv(override=True)

api_key = os.getenv("OPEN_AI_SECRET_KEY")
client = OpenAI(api_key=api_key)

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
        "size": 170  # 한 번에 가져올 문서 수
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

def chunk_logs(logs, chunk_size=170):
    """
    로그 데이터를 chunk_size 개수로 나눕니다.
    """
    for i in range(0, len(logs), chunk_size):
        yield logs[i:i + chunk_size]


def extract_cloudTrail():

    # Elasticsearch에서 로그 가져오기
    logs = fetch_all_logs_with_scroll()

    if not logs:
        print("가져온 로그가 없습니다. 작업을 종료합니다.")
        return

    template_content = load_prompt(prompt_files["daily"])  # 파일 내용을 읽어옴

    # 청크 데이터를 리스트로 변환
    log_chunks = list(chunk_logs(logs, 170))
    print(f"총 {len(log_chunks)}개의 청크로 나누어졌습니다.")

    # 각 chunk에 대해 ChatGPT API 호출
    response_list = []  # 각 chunk 응답 저장 리스트
    for index, log_chunk in enumerate(log_chunks, start=1):

        print(f"Chunk {index} 시작: {len(log_chunk)}개의 로그를 처리 중입니다.")
        
        # 로그 데이터를 문자열로 변환
        log_string = "\n".join(str(log) for log in log_chunk)

                # 템플릿 복사 후 데이터 삽입
        current_template = template_content  # 원본 템플릿 유지

        try:
            formatted_prompt = current_template.format(logs=log_string)
        except Exception as e:
            print(f"Chunk {index} 템플릿 포맷팅 중 오류 발생: {e}")
            continue

        prompt_txt = {"daily": {"role": "system", "content": formatted_prompt}}

        # ChatGPT API 호출
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
            continue

    # 저장된 응답으로 최종 요약 생성
    if response_list:
        try:
            combined_prompt = "\n".join(response_list) + "\n데이터의 관계와 흐름을 파악해서 요약하세요."
            final_summary = text_response(client, "gpt-4o-mini", [{"role": "user", "content": combined_prompt}])
            print_response("최종 요약", final_summary)
            save_history([{"role": "summary", "content": final_summary}], "final_summary.txt", append=True)

        except Exception as e:
            print(f"최종 요약 생성 중 오류 발생: {str(e)}")


if __name__ == "__main__":
    # 실행 시간 측정 시작
    start_time = time.time()
    extract_cloudTrail()
    # 실행 시간 측정 종료
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"실행 시간: {elapsed_time:.2f}초")
