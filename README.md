ROS 2 – MariaDB 연동하기 
                                           

MariaDB의 Host , User , Password, DB 이름을 설정한다. 


MariaDB 에게 Python Msg를 보내는 형식 -> DBSubscriber Class 생성

< DB와 연결하는 함수 생성 >

-> python 인스턴스 생성 (클래스의 정의된 함수를 사용하기 위해)

-> ros init 생성 

   1. DB와 연동하는 함수 -> db_connection 생성

   2. ROS2 내의 로봇의 Cmd_vel msg -> db_connection
     - 로봇의 속도를 알기 위해서 db에 데이터 저장
     - Twist의 지정된 robot_namespace의 Cmd_vel 값을 저장

   3. ROS2 내의 로봇의 Scan Callback msg -> db_connetion
     - 로봇이 장애물을 탐지할 때 장애물과 로봇의 거리 경고메세지 생성 및 db에 데이터 저장
    
   4. ROS2 내의 로봇의 Odometry 값 -> db_connetion
     - 로봇의 현재 위치를 알기 위해서 odom값 db에 저장


< 생성된 함수 정의하기 >

-> MariaDB 와 연결하는 함수 정의하기 

-> DB Config 사용해 DB 연동의 편의성을 높이기

-> Twist의 Cmd_vel topic msg를 callback

-> ROS로 제어하는 로봇은 Cmd_vel 속도 명령을 보내서 구동한다. 

-> 제어하는 Cmd_vel 속도 명령 토픽을 콜백하여 MariaDB의 데이터를 보냄

-> Twist의 pose topic msg를 callback

-> 로봇의 현재 위치를 파악하기 위해 Pose x,y,z 값을 측정 후 MariaDB에 데이터를 보냄

-> 현재 위치와 속도 명령 2가지이 로봇의 기본적인 움직임을 파악하는 가장 중요한 요소들이라 판단하여 2가지 데이터를 DB에 넣고자 하였다. 

-> 향후 로봇의 기본적인 값들을 계속 추가하여 완성도를 높일 예정
   Ex) 로봇의 종류, 로봇의 이름 (네임스페이스) , 목적지, 받은 명령

-> 로봇의 시나리오를 하나 가정해서 경고 메시지를 DB에 보냄

-> 로봇이 위험물을 탐지할 시 경고 신호를 보내는 시나리오

-> Scan data의 180도 안에 장애물이 1m 이내 탐지되면 로봇의 경고 메시지를 MariaDB에 보낸다. (Warn or Fetal)

-> 그때 위험한 로봇의 namespace_id와 speed 값을 MariaDB 안에 넣는다.
  
-> 향후 경고 신호 탐지 시 로봇을 강제로 멈추는 코드 구성을 생각

-> 로봇을 운영할 때 중요한 요소 중 하나인 안정성에 대해서 필요한 부분이라 가장 먼저 생각한 시나리오라서 구현

< ROS – DB Connetion 마무리 Code > 

