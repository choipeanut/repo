# Position Based Dynamics (PBD) 구현

이 저장소는 Müller et al. (2007) Position Based Dynamics의 핵심 아이디어를 작은 예제로 구현한 프로젝트입니다.

## 포함 내용

- 입자 시스템 (`ParticleSystem`)
- 거리 제약 (`DistanceConstraint`)
- 반복 투영 시뮬레이터 (`PBDSimulator`)
- 콘솔 체인 데모 (`examples/chain_demo.py`)
- 웹 기반 상호작용 옷감(Cloth) 데모 (`examples/interactive_cloth.html`)

## 실행

### 1) 콘솔 데모

```bash
python examples/chain_demo.py
```

### 2) 상호작용 Cloth 데모 (브라우저)

```bash
cd examples
python -m http.server 8000
```

브라우저에서 `http://localhost:8000/interactive_cloth.html`을 엽니다.

조작법:
- 마우스 드래그: 천을 잡아당기기
- `r`: 초기 상태 리셋

## 테스트

```bash
pytest -q
```
