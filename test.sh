#!/bin/bash

#코드 실행에 필요한 환경변수를 선언합니다.
export HSA_OVERRIDE_GFX_VERSION=10.3.0
export ROCM_PATH=/opt/rocm-5.5.1/

# conda 가상환경을 활성화 합니다.
source /home/lee99/anaconda3/etc/profile.d/conda.sh
conda activate ldm

# 꿈 내용을 사용자로 부터 입력 받습니다.
echo "Enter your dream: "
read prompt
echo "your dream is: $prompt"

# 이미지 생성을 위한 시드 숫자를 입력 받습니다.
echo "Enter seed number: "
read seed

# stable-diffusion모델이 설치된 디렉토리로 이동합니다.
cd  /home/lee99/stable-diffusion/ 
# 프롬포트 내용을 바탕으로 이미지 2장을 생성합니다.
python3 optimizedSD/optimized_txt2img.py --prompt="${prompt}" --n_samples 2 --seed $seed

# stablelm 코드가 작성된 디렉토리로 이동합니다.
cd /home/lee99/PycharmProjects/pythonProject3/
# 프롬프트 내용을 바탕으로 글을 생성합니다.
python3 stableLM.py --prompt="${prompt}"

# 생성한 글과 그림을 바탕으로 에 글을 작성합니다.
python3 word.py --prompt="${prompt}" --seed=$seed

prompt=${prompt//" "/"_"}
# 생성한 파일을 열어 줍니다.
libreoffice --writer /home/lee99/문서/AI_bigdata/dream_story/my_dream-${prompt}.docx
