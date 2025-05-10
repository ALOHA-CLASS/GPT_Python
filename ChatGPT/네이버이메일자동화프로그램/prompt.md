
페르소나
- 파이썬 프로그래밍 학습자
작업
- 네이버 이메일 자동화 프로그램 개발
맥락
- 언어 : 파이썬
- 버전 : 3.13
- 구조 : GUI 프로그램
- 기능
* MySQL 데이터베이스에 이메일 데이터를 저장
- 받는사람 메일주소, 제목, 내용, 상태(완료,전송전)
- 프로그램 실행 시, email 테이블 없으명 생성
- database=python, useranme=python, password=123456

* 일괄전송 기능
- "일괄전송" 버튼을 누르면, 데이터베이스에서 이메일 정보를 조회하여
  순차적으로 메일을 전송하는 기능
- 로그인 여부 확인 후, 메일 쓰기 진행
- 이메일 쓰기 url : https://mail.naver.com/v2/new
- 입력 태그
  * 이메일  : id="recipient_input_element"
  * 제목    : id="subject_title"
  * 내용    : class="workseditor-content"
- 전송 버튼
  * class="button_write_task"
- 전송 후, 
  https://mail.naver.com/v2/new/done 경로로 이동될 때까지 대기
  https://mail.naver.com/v2/new/done 완료 페이지로 이동 되면 
  해당 이메일 정보는 DB에서 status 완료로 변경후, 
  완료가 아닌 다음 이메일 보내기 진행

- 모든 이메일 전송이 완료되면, 팝업창으로 안내 메시지 출력

* 네이버 자동 로그인 기능
- 아이디, 비밀번호를 입력해놓고 로그인 버튼 클릭 시, 네이버에 로그인
  url : https://nid.naver.com/nidlogin.login?mode=form
형식
- 파이썬 GUI 프로그램에서 크롬 웹브라우저를 제어하는 방식
예시
- 아이디 비번 입력 후, 로그인 버튼 클릭 시 브라우저에서 네이버에 로그인
- 메일 등록 버튼 클릭 후, 이메일주소, 제목, 내용 작성 후 저장하면
  email 테이블에 이메일 정보 등록
- 메일 정보 삭제, 수정 처리
- "일괄 전송" 버튼 클릭 시, 읽어드린 이메일 목록을 순차적으로 전송

캔버스 모드로 응답