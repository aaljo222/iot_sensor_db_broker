# IoT 센서 → Supabase 인제스트 서비스

**MQTT로 올라오는 센서 텔레메트리를 구독해, 파싱한 뒤 Supabase(Postgres)에 저장하는 FastAPI 백엔드.**

> 디바이스 → 네트워크 → **저장**으로 이어지는 IoT 파이프라인의 **수집·영속화(ingest) 측**입니다. STM32 등 센서 노드가 MQTT 브로커에 발행하면, 이 서비스가 구독해 JSON을 파싱하고 Supabase 테이블에 적재합니다. (실시간 시각화 측은 별도 대시보드 레포)

---

## 파이프라인

```
센서 노드(STM32 등)  ──MQTT(TLS)──▶  브로커  ──▶  [ 이 서비스 ]  ──insert──▶  Supabase (Postgres)
                        sensor/#            FastAPI · paho-mqtt              sensor_data 테이블
```

## 무엇을 하나

- 앱 기동 시 **MQTT 브로커에 TLS(8883)로 접속** → 토픽 **`sensor/#`** 구독
- 메시지 수신 시 payload(JSON)를 파싱해 **Supabase `sensor_data` 테이블에 insert**
  - `device_id` — 토픽 `sensor/<device_id>/...`에서 추출
  - `topic` — 원본 토픽 문자열
  - `payload` — JSON 본문(그대로 저장)
- **헬스체크 엔드포인트** `GET /` → `{"status": "ok"}` (배포 상태 확인용)

## 저장 스키마 (`sensor_data`)

| 컬럼 | 내용 |
|------|------|
| `device_id` | 토픽에서 파싱한 디바이스 식별자 |
| `topic` | 수신한 MQTT 토픽 |
| `payload` | 센서 JSON 페이로드 (jsonb) |

## 실행

```bash
pip install -r requirements.txt
# 아래 환경변수 설정 후
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 설정 (환경변수)

자격증명은 코드에 하드코딩하지 않고 환경변수(.env)로 주입합니다.

```bash
MQTT_HOST=your-broker-host        # MQTT 브로커 (TLS 8883)
MQTT_USERNAME=your_user
MQTT_PASSWORD=your_pass
# Supabase 접속 정보(URL·API Key)는 supabase_client.py / .env 에 설정
```

## 스택

FastAPI · Uvicorn · **paho-mqtt**(MQTT 구독, TLS) · **supabase-py**(Postgres 적재) · python-dotenv

## 구성

| 파일 | 역할 |
|------|------|
| `main.py` | FastAPI 앱 — 기동 시 MQTT 시작, `GET /` 헬스체크 |
| `mqtt_client.py` | MQTT 접속·구독(`sensor/#`)·메시지 수신 → Supabase insert |
| `supabase_client.py` | Supabase 클라이언트 초기화(URL·Key) |
| `requirements.txt` | 의존성 |

---

**이재오** · (주)에이아이컴퍼니 · ceo@aicompany.co.kr · [github.com/aaljo222](https://github.com/aaljo222)
IoT 데이터 파이프라인 · MQTT · FastAPI · Supabase — 센서에서 데이터베이스까지.
