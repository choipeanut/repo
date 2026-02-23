# Position Based Dynamics (PBD) 구현

이 저장소는 Müller et al. (2007) Position Based Dynamics 논문의 핵심 루프를 **일반 PBD** 형태로 구현한 예제입니다.

## 포함 내용

- 입자 시스템 (`ParticleSystem`)
- 거리 제약 (`DistanceConstraint`)
- 반복 투영 시뮬레이터 (`PBDSimulator`)
- 콘솔 데모 (`examples/chain_demo.py`)
- 시각화 + 상호작용 데모 (`examples/interactive_chain.py`, tkinter 기반)

## 빠른 실행

```bash
python examples/chain_demo.py
```

```bash
python examples/interactive_chain.py
```

상호작용 데모 조작법:
- 마우스 좌클릭 드래그: 고정되지 않은 입자 이동
- `r`: 초기 상태로 리셋

## 테스트

```bash
pytest -q
```

## 알고리즘 개요

1. 속도에 외력을 적용하고 예측 위치를 계산.
2. 제약 조건을 여러 번 투영(iterative projection)해 만족시킴.
3. 보정된 위치와 이전 위치 차이로 새 속도를 계산.

거리 제약은 XPBD의 compliance 항을 사용하여 강체/유연체 특성을 조절할 수 있습니다.
