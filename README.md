## 들어가기 앞서
진짜맛집 프로젝트는 인스타그램에서 맛집검색을 할때, 
맛집과는 관련없는 허위성 게시물을 필터링해서 보여주는 프로젝트다.
이 프로젝트는 그중에서 백엔드 부분에 해당한다.

이 서버 안에는 api서버, 크롤링, 오브젝트디텍션 3가지 기능이 모두 들어있다.
첨에는 뭣도 모르고 한프로그램안에 기능이 다 들어있으면 좋지 않을까 생각했는데
분리를 안해놓으면 서로 얽히고설켜서 한 부분의 수정이 다른쪽 기능에 큰 영향을 준다.
한마디로 의존성이 커진다.

앞으로는 이 기능들을 각각 마이크로 아키텍쳐단위로 분리하고
서로통신을 통해 작동하도록 의존성을 줄이는 방향으로 수정될것이다.
분리되기 때문에 다른 레포에 각각 올라간다.

오브젝트 디텍션부분은 yolo v4의 오픈소스코드를 수정해서 사용하였다.

## 요구사항

### Conda
이 프로젝트는 콘다환경이 설치되어있어야한다. 아나콘다를 추천
가상환경을 설정하는데
gpu가 없는 환경이면 yolov4-cpu
있으면 아래 yolov4-gpu 가상환경을 설정한다.

```bash
# Tensorflow CPU
conda env create -f conda-cpu.yml
conda activate yolov4-cpu

# Tensorflow GPU
conda env create -f conda-gpu.yml
conda activate yolov4-gpu
```

### 인스타그램 계정
크롤링에 활용할 계정이 필요하다.
용도가 용도인 만큼 언제든 버려질 계정을 새로 파서 하는것을 추천.
프로젝트 폴더의 insta.py의 open_driver()함수안의 변수에 아이디 비밀번호를 입력한다.

### weight파일
음식데이터로 학습된 가중치파일을 다운받아 프로젝트 폴더의
data/ 안에 넣는다.
custom weights : https://github.com/Qone2/real-matzip-backend/releases/download/v0.0.1/custom.weights

### chrome webdriver
자신의 버전에 해당하는 크롬웹드라이버를 프로젝트 폴더에 위치시킨다.

## Getting Started

### Convert
먼저 .weights파일을 tenserflow model file로 변경한다.

```bash
# Convert darknet weights to tensorflow

python save_model.py --weights ./data/custom.weights --output ./checkpoints/custom-416 --input_size 416 --model yolov4 

```

### Migrate
장고프로젝트에서 마이그레이트 시키고
```
python manage.py migrate
```
웹드라이버가 실행돼도 당황하지 말고 터미널에서 마이그레이트가 끝나면 웹드라이버를 닫아도 된다.

### Runserver
서버를 실행한다.
```
python manage.py runserver <port num(default:8000)>
```
웹드라이버가 실행되면 닫지 말고 서버를 종료시킬 때까지 켜둔채로 유지한다.

## Spacific
### 기본 api
서버 실행 후
http://localhost:8000/matzip/
로 들어가면 프로젝트를 위한 기본 api 응답이 나온다.
포스트주소, 이미지주소, 해쉬태그 검색 키워드, 그리고 음식과 관련된 내용인지에 대해서 나온다. allowed가 true면 음식과 관련된 포스트란 뜻.

### 크롤링 및 딥러닝 요청
api서버에 아무런 내용이 없다면 다음과 같은 방법으로 크롤링 및 posting을 할 수 있다.  
http://localhost:8000/insta_deep/<해쉬태그검색어 (ex: 홍대맛집)>  
에 GET요청을 보내면 서버에서 해당검색어로 크롤링과 딥러닝을 하여 결과를 http://localhost:8000/matzip/에 POST한다.

### Image url
api서버의 이미지url을 브라우저에서 여는건 가능하지만 스크립트에서 사용하면 CORS문제로 참조불가능 할것이다. 크롤링 작업과정에서 사진을 프로젝트의 media폴더에 저장하며, 
http://localhost:8000/media/<파일명.jpg> 에서 CORS문제없이 열람가능하다.  
파일명은 포스트주소에서 마지막 랜덤값을 자른 것 이다.

### 검색기능
api응답 내에서 keyword에 대하여 http://127.0.0.1:8000/matzip/?search=<검색어>
로 쿼리하여 응답을 받을 수 있다.




## References

  * YOLOv4: Optimal Speed and Accuracy of Object Detection [YOLOv4](https://arxiv.org/abs/2004.10934).
  * [darknet](https://github.com/AlexeyAB/darknet)
  
  여기 프로젝트를 적극적으로 활용하였음
  * https://github.com/theAIGuysCode/tensorflow-yolov4-tflite

   and his project is inspired by these previous fantastic YOLOv3 implementations:
  * [Yolov3 tensorflow](https://github.com/YunYang1994/tensorflow-yolov3)
  * [Yolov3 tf2](https://github.com/zzh8829/yolov3-tf2)