

```text
Network Working Group                                         G. Deloche
Request for Comments: 11                                            UCLA
                                                             August 1969

                   Implementation of the Host - Host
                      Software Procedures in GORDO
```

---
# **TABLE OF CONTENTS**

```text
   Chapter                                                        Page
   -------                                                        ----
   1.  Introduction . . . . . . . . . . . . . . . . . . . . . . .   1
   2.  HOST - HOST Procedures . . . . . . . . . . . . . . . . . .   2
       2.1  Generalities  . . . . . . . . . . . . . . . . . . . .   2
       2.2  Connections and Links . . . . . . . . . . . . . . . .   2
            2.2.1  Definitions  . . . . . . . . . . . . . . . . .   2
            2.2.2  Connection types . . . . . . . . . . . . . . .   3
       2.3  Message Structure . . . . . . . . . . . . . . . . . .   5
       2.4  User Transactions . . . . . . . . . . . . . . . . . .   6
            2.4.1  List of transactions   . . . . . . . . . . . .   7
            2.4.2  HOST-HOST protocol and control messages  . . .   8
   3.  Implementation in GORDO  . . . . . . . . . . . . . . . . .  11
       3.1  Introduction to GORDO . . . . . . . . . . . . . . . .  11
            3.1.1  GORDO file system  . . . . . . . . . . . . . .  11
            3.1.2  GORDO process  . . . . . . . . . . . . . . . .  12
       3.2  Software Organization Overview  . . . . . . . . . . .  12
       3.3  Software Description  . . . . . . . . . . . . . . . .  13
            3.3.1  Data structures  . . . . . . . . . . . . . . .  13
                   3.3.1.1  Allocation tables . . . . . . . . . .  13
                   3.3.1.2  Buffer pages  . . . . . . . . . . . .  16
            3.3.2  Programs . . . . . . . . . . . . . . . . . . .  18
                   3.3.2.1  Handler . . . . . . . . . . . . . . .  18
                   3.3.2.2  Network . . . . . . . . . . . . . . .  19
       3.4  Software Procedures . . . . . . . . . . . . . . . . .  20
            3.4.1  Description of some typical sequences  . . . .  20
   Appendix A:  Flowcharts  . . . . . . . . . . . . . . . . . . .  23
```

```text
   [[RFC Editor Note: [s] represents subscript s]]
```

---
## **1.  INTRODUCTION**

이 기술 노트는 \(1\) HOST-HOST 절차와 \(2\) GORDO\(UCLA HOST 운영 체제\)에서 해당 프로그램의 구현에 중점을 둡니다.

첫 번째 섹션은 BBN 보고서 번호 1822 및 1763\[1\]과 밀접하게 관련되어 있으며 메시지 교환을 위한 HOST 기능을 지정합니다. 주로 링크와 연결, 메시지 구조, 트랜잭션, 제어 메시지를 다룬다.

두 번째 섹션은 소프트웨어 중심입니다. HOST 기능이 GORDO에 어떻게 구현되고 통합되는지 설명합니다. 데이터 구조, 프로그램, 버퍼, 인터럽트 처리 등과 관련됩니다.

\[1\] 이 섹션의 일부는 해당 보고서에서 가져왔거나 참조되었습니다.

---
## **2.  HOST-HOST PROCEDURES**
---
## **2.1  Generalities**

기본 아이디어는 주어진 HOST에서 여러 사용자가 물리적 시설을 시분할하여 동시에 네트워크를 활용할 수 있어야 한다는 것입니다.

이는 각 HOST 운영 체제 내에 사용자로부터 나가는 메시지를 네트워크로 다중화하고 들어오는 메시지를 적절한 사용자에게 배포하는 특수 프로그램이 있어야 함을 의미합니다. 우리는 이 특별한 프로그램을 네트워크 프로그램이라고 부르겠습니다.

---
## **2.2  Links and Connections  (See figure 1)**

```text
   2.2.1  Definitions
```

네트워크를 호스트 컴퓨터 쌍이 아닌 원격 사용자 간에 메시지를 통신하기 위한 블랙박스\(동작은 알려져 있지만 메커니즘은 알려지지 않은 시스템\)로 간주하는 것이 편리합니다.

```text
      (a)  Logical connections
```

- 원격 HOST에 있는 두 사용자를 연결하는 통신 경로로 논리적 연결을 정의합니다.

- 이 개념을 사용하면 HOST 컴퓨터의 사용자\(사용자 프로그램\)는 \(1\) 원격 HOST 사용자에게 여러 논리적 연결을 설정하고 \(2\) 해당 연결을 통해 메시지를 보내거나 받을 수 있습니다.

- 연결은 사용자에게 전이중으로 나타납니다.

- 네트워크 프로그램의 목적 중 하나는 이러한 연결을 설정, 식별 및 유지하는 데 있어 사용자에게 서비스를 제공하는 것입니다.

```text
      (b)  Logical links
```

- 각 논리적 연결은 한 쌍의 방향 링크로 구성됩니다. 하나는 전송용이고 다른 하나는 수신용입니다.

- 논리 링크라고 불리는 이러한 링크는 네트워크 프로그램에 의해 설정되고 사용됩니다.

- 여기서 사용자는 연결에만 관심이 있고 링크에 대해서는 전혀 인식하지 못한다는 점에 유의하세요. 링크와 연결 사이의 관계는 네트워크 프로그램에 의해 수행됩니다.

- 연결을 한 쌍의 방향 링크로 정의하는 장점 중 하나는 HOST가 IMP를 통해 자신을 루프할 수 있다는 것입니다\(자신에게 연결을 엽니다\). 이 기능은 디버깅 목적으로 유용할 수 있습니다.

- 이 문서를 통해 더 이상 링크나 연결을 참조할 때 논리적 속성을 사용하지 않을 것입니다.

```text
   2.2.2  Connection types
```

네트워크 활용 시 높은 유연성을 얻으려면 연결을 분류하는 것이 좋습니다.

\(a\) 제어 연결, \(b\) 기본 연결, \(c\) 보조 연결의 세 가지 유형의 연결이 구별됩니다.

```text
      (a)  Control connection
```

- 이 연결은 특별한 상태를 가지며 HOST 쌍 사이에서 고유합니다. 예를 들어 네트워크에 x HOST가 포함된 경우 하나의 HOST에서 발행된 최대 x 개의 제어 연결이 있습니다.

```text
      This connection is used by remote Network programs for passing
      control messages back and forth.  Control messages are basic to
      the establishment/deletion of standard connections.  (See 2.4.2)
```

- 여기서 이 제어 연결은 HOST 사용자가 사용하지 않는 유일한 연결입니다.

- 이제 표준 연결에 대해 설명하겠습니다.

```text
      (b)  Primary connection

      These connections connect remote users.
```

- 기본 연결:

- \*는 사용자 쌍 간에 고유하며 가장 먼저 설정됩니다.

\* "텔레타이프와 유사"합니다. 즉:

- - ASCII 문자가 전송됩니다. - 에코는 원격 호스트에 의해 생성됩니다. - 수신 HOST는 구분 문자를 검색합니다. - 전송 속도가 느립니다\(20자/초 미만\).

- \* 주로 원격 HOST 운영 체제에 로그인하는 등 제어 명령을 전송하는 데 사용됩니다.

```text
      (c) Auxiliary connection

         These connections also connect remote users:
```

- 보조 연결:

- \* 기본 연결과 병렬로 열리며 고유하지 않습니다. 즉, 사용자 간에 여러 보조 연결을 설정할 수 있습니다.

- \* 대용량 데이터 전송에 사용됩니다\(파일 지향\).

- \* 바이너리 또는 문자 전송에 사용됩니다.

- \[그림 1 - 링크 및 연결 - PDF 파일 참조\]

---
## **2.3  Message Structure**

HOST는 메시지를 통해 서로 통신합니다. 메시지의 길이는 최대 8095비트까지 다양합니다\(아래 구조 참조\). 따라서 더 큰 전송은 HOST 사용자에 의해 이러한 메시지의 시퀀스로 분할되어야 합니다.

- 메시지 구조는 그림 2와 같습니다.

- 여기에는 다음이 포함됩니다.

```text
      (1) A leader (32 bits): Message type, Source/Destination HOST,
          link number.  (See BBN report No. 1822, pp 13, 17)

      (2) A marketing (32 bits when sent by the Sigma 7) for starting a
          message text on a word boundary.  (See BBN report No. 1822,
          pp. 17, 19)

      (3) The message text (Max: 8015 bits for the Sigma 7).  It mostly
          consists of user's text.  However, it may represent
          information for use by the Network programs.  (Control
          messages, see 2.4.2)
```

- \(4\) 체크섬\(16비트\). 그 목적은 HOST 수준에서 메시지가 올바르게 전송되었는지 확인하는 것입니다. \(비트 패턴 또는 패킷 전치의 변경, 패킷은 BBN 보고서 번호 1763, 13페이지에 정의되어 있습니다.\) 체크섬 계산은 아래를 참조하세요.

- \(5\) 단어 길이 불일치 문제를 해결하기 위한 패딩. \(BBN 보고서 번호 1822, 17, 19페이지 참조\). 소프트웨어에 관한 한 패딩은 메시지 끝을 묘사하기 위한 메시지 수신에만 관련됩니다. \(전송 시 하드웨어가 패딩을 관리합니다.\)

```text
   Remark:

      Checksum calculation:
```

- HOST가 보낸 모든 메시지의 마지막 16비트는 체크섬입니다. 이 체크섬은 표시를 포함하여 전체 메시지에 대해 계산되지만 32비트 리더와 패딩은 제외됩니다. 체크섬을 계산하려면 다음을 수행하십시오.

- 1. 8640비트 길이까지 0으로 채워지는 메시지를 고려하세요.

- 2. 8640비트를 6개의 1440비트 세그먼트 S0, S1...S5로 분할합니다.

- 3. 각 1440비트 세그먼트 S를 90개의 16비트 요소 T0, T1...T89로 분할합니다.

- 4. 두 개의 16비트 요소를 입력으로 사용하고 16비트 요소를 출력하는 함수 \[\(+\)\]를 정의합니다. 이 함수는 다음과 같이 정의됩니다.

```text
          Tm [(+)] Tn = Tm [(+)] Tn, if Tm + Tn < 2[exp 16]

          Tm [(+)] Tn = Tm [(+)] Tn - 2[exp 16] + 1, if Tm + Tn >= 2[exp
          16]
```

- 5. 각 1440비트 세그먼트 Si에 대해 Ci = K\(Si\)를 계산합니다. 여기서

```text
          K(S) = T0 [(+)] T1 + ..... T89

      6.  Computer C =
          C0[(+)]C1[(+)]C1[(+)]C2[(+)]C2[(+)]C2[(+)]C2....[(+)]C5

          (Notice that C1[(+)]C1 is just C1 rotated left one bit)
```

숫자 C는 체크섬입니다. Ci를 i비트씩 회전시키는 이유는 패킷 전치를 감지하기 위함이다.

\[그림 2 - Sigma 7에서 보내는 메시지 형식 - PDF 파일 참조\]

---
## **2.4  User Transactions**

지금까지 논의한 내용에서 네트워크는 사용자에게 연결 묶음으로 나타납니다. 이제 이러한 연결을 어떻게 활용할 수 있는지 설명하겠습니다.

먼저, 연결 기능을 활용하기 위해 사용자가 액세스할 수 있어야 하는 일련의 트랜잭션을 설명하겠습니다.

그런 다음 이러한 트랜잭션을 실행하기 위한 네트워크 프로그램의 역할을 설명하겠습니다. 이는 네트워크 프로그램 간에 제어 메시지가 교환되는 HOST-HOST 프로토콜을 다룹니다.

설명을 위해 이러한 트랜잭션은 사용자 수준에서 서브루틴 호출 및 매개변수의 형태로 표시됩니다. 그러나 이는 구현이 이 패턴을 밀접하게 따른다는 것을 전혀 의미하지 않습니다. \(여기서는 구현 측면보다 설명에 더 관련되어 있습니다. 3장을 참조하세요.\)

2.4.1 거래 목록

아래 목록은 연결을 생성/끊고 이를 통해 데이터를 전송/수신하기 위해 사용자가 사용할 수 있는 서브루틴에 대한 설명입니다. 이 서브루틴 세트는 사용자 수준과 네트워크 프로그램 수준 사이의 일종의 인터페이스로 간주될 수 있습니다.

```text
   (a)  Open primary connection:
```

OPENPRIM\(연결 ID, HOSTID, BUFFADDR, \[OPT\]\)

- CONNECTID: 연결 식별 # HOSTID: 원격 HOST 식별 # BUFFADDR: 수신 메시지에 대한 버퍼 주소. OPT: 성공적인 연결 설정 후 필요한 메시지, "전체 에코"\(각 메시지는 확인 목적으로 원격 호스트에 의해 다시 전송됨\) 등과 같은 옵션입니다.

```text
        Remark: [  ] means optional

   (b) Open auxiliary connection
```

OPENAUX\(CONNECTID, BUFFADDR, N, \[OPT\]\)

- CONNECTID: 연결 식별 #, 즉 해당 기본 연결의 ID\(먼저 사용자가 기본 연결을 열어야 함\). BUFFADDR: 위와 같은 의미입니다. N: 열려야 하는 보조 연결 수입니다. OPT: 위와 같은 의미입니다.

\(c\) 연결을 통한 전송

전송\(연결 ID, NO, BUFFADDR, N, \[OPT\]\)

- CONNECTID: 연결 식별 # NO: 연결 #. 기본 연결은 항상 NO=0으로 참조됩니다. 보조 연결 번호는 설정된 순서에 해당합니다. \(열린 첫 번째 보조는 NO=1로 참조되고, 두 번째 보조는 NO=2로 참조됩니다.\) BUFFADDR: 전송할 메시지의 버퍼 주소입니다. N: 메시지 크기\(바이트 수\) OPT: 데이터 유형\(문자 대 바이너리\), 추적 비트 등과 같은 옵션

```text
   (d)  Close connection
```

닫기\(연결 ID, \[N\], \[NO\]\)

- CONNECTID : 연결식별번호. N: 닫을 연결 수입니다. 생략하면 기본 링크를 포함하여 사용자가 사용 중인 모든 연결이 닫힙니다. NO: N이 0이 아닌 경우 이 숫자는 닫힐 보조 연결 #을 나타냅니다.

2.4.2 HOST-HOST 프로토콜 및 제어 메시지

HOST-HOST 프로토콜은 네트워크 프로그램에 의해 수행됩니다. 이는 주로 이전 트랜잭션\(사용자가 시작한\)의 실행을 포함하며 HOST-HOST 대화를 다룹니다.

이 대화는 연결을 열거나 끊는 제어 절차를 수행하며 제어 링크를 통해 제어 메시지를 교환하는 것으로 구성됩니다. 제어 메시지는 일반 메시지와 동일한 구조를 가지고 있습니다. 사용자 대신 네트워크 프로그램이 사용하는 텍스트만 다릅니다.

이 제어 절차는 IMP 컴퓨터에 구현된 전송 제어 절차와 전혀 관련이 없다고 주장하겠습니다. 우리는 호스트 수준\(네트워크 프로그램\)에 있으므로 아래에서 설명할 제어 메시지는 일반 메시지처럼 IMP를 통해 전송됩니다.

이제 이전 트랜잭션을 고려하고 각 트랜잭션에 대해 어떤 메시지가 어떤 링크를 통해 교환되는지 설명하십시오. 각 사례는 간단한 예를 통해 설명됩니다.

HOST\(x\) 사용자가 URSA라는 원격 HOST\(y\) 프로그램을 원한다고 가정합니다.

```text
      (a)  Open a primary connection: (OPENPRIM)
```

- HOST\(x\)의 네트워크 프로그램은 기본 연결 열기를 사용하여 깨어나\(3.3 참조\) HOST\(y\)의 네트워크 프로그램과 대화를 시작합니다.

- \(i\) HOST\(x\)는 다음 제어 메시지를 보냅니다:

```text
             HOST(x)       Control link                      HOST(y)
                         -------------------->
                           ENQ PRIM 0 1 2
```

- ENQ: 연결 설정 문의\(ASCII 문자 1개\) PRIM: 연결 유형: 기본\(특수 문자 1개\) 0 1 2: 나가는 링크 #. 이는 10진수\(ASCII 문자 3개\)입니다\(예: 링크 #12\).

```text
                      This link # has been determined by the HOST(x)
                      Network program (See implementation: 3.3)
```

- \(ii\) HOST\(y\)는 다음 제어 메시지를 다시 전송하여 확인합니다.

```text
             HOST(x)        Control link                     HOST(y)
                         <------------------------
                          ACK ENQ PRIM 0 1 2 0 1 5
```

- ACK: 긍정적인 승인\(ASCII 문자 1개\) ENQ PRIM 0 1 2: 위와 같은 의미. 메시지의 이 부분은 확인 목적으로 반환됩니다. 0 1 5: 들어오는 링크 #. 나가는 링크 #과 동일한 패턴을 따릅니다. 이 링크 #은 HOST\(y\) 네트워크 프로그램에 의해 결정되었습니다.

- 이제 연결이 설정되었습니다. 사용자 메시지 교환을 위해 링크 #12와 15를 사용합니다. 연결은 로그인 전 상태에 있다고 합니다. 즉, 원격 HOST\(y\)는 표준 로그인 절차를 기대합니다.

```text
      (b)  Transmission over primary connection: (TRANSM)
```

- 기본 연결을 참조하는 TRANSM 서브루틴을 통해 HOST\(x\) 사용자는 HOST\(y\) 운영 체제에 로그인한 다음 URSA 프로그램\(HOST\(y\) 사용자 프로그램\)을 호출할 수 있습니다.

- 양쪽 끝의 네트워크 프로그램은 메시지 전달을 위해 링크 #12와 #15를 사용합니다. 이러한 메시지는 내용이 로그인 순서에 사용되는 표준 메시지입니다.

- 간단한 예는 다음과 같습니다.

```text
             HOST(x)     Prim. Link #12                       HOST(y)
                         ---------------------------->
                         ! S I G N - I N : X X

             HOST(x)     Prim. Link #15                       HOST(y)
                         <--------------------------
                         ! ! R E A D Y

             HOST(x)     Prim. Link #12                       HOST(y)
                         ---------------------------->
                           ! U R S A

      (c)  Open an auxiliary connection: (OPENAUXI)
```

- \(a\)와 매우 유사한 방식으로 HOST\(x\)와 HOST\(y\) 사이에 보조 연결이 설정됩니다. 이를 위해 제어 메시지는 제어 링크를 통해 교환됩니다.

```text
             HOST(x)           Control link                  HOST(y)
                         ------------------------------>
                               ENQ AUX 0 2 5

             HOST(x)           Control link                  HOST(y)
                         <--------------------------------
                             ACK ENQ AUX 0 2 5 0 2 1
```

- 이제 보조 연결이 설정되었으며 표준 메시지 교환을 위해 링크 #25 및 21을 사용합니다.

```text
      (d)  Transmission over auxiliary connection: (TRANSM)
```

- 보조 연결을 참조하는 TRANSM 서브루틴을 통해 양쪽 끝의 사용자가 데이터를 교환할 수 있습니다.

```text
             HOST(x)        Aux. Link #25                    HOST(y)
                         -------------------------------->
                               X X ..... X X

             HOST(x)         Aux. Link #21                   HOST(y)
                         <--------------------------------
                             X ......... X

         etc.......

      (e)  Close connections: (CLOSE)
```

- \(a\)와 같은 방식으로 진행된다. 사용자가 CLOSE 서브루틴을 호출하면 양쪽 끝의 네트워크 프로그램이 제어 메시지를 교환합니다.

```text
             HOST(x)           Control Link                  HOST(y)
                         ----------------------------->
                               EOT 0 0 1 0 1 2
```

EOT: 전송 끝\(ASCII 문자 1개\)

- 0 0 1 : 닫을 연결 수\(10진수 ASCII 문자 3개\) 0 1 2 : 닫을 나가는 링크 #.

- 그러면 HOST\(y\)는 \(a\)와 같이 다시 응답합니다.

```text
             HOST(x)           Control Link                  HOST(y)
                         <-----------------------------
                            ACK EOT 0 0 1 0 1 2 0 1 5
```

- 참고 1 - \(a\), \(c\), \(e\)에서 HOST\(y\)는 ACK 대신 부정 응답 문자 NAK를 포함하는 메시지에 응답할 수 있습니다. 이는 잘못된 순서, 이미 열린 연결 등 다양한 이유 때문에 발생합니다. 메시지는 NAK IND일 수 있습니다. 여기서 IND는 이전 블록이 거부된 이유를 코딩된 형식으로 나타내는 영숫자 문자입니다. 이러한 승인을 다시 받으면 HOST\(x\)는 HOST\(y\)가 이를 수락할 때까지 메시지를 반복합니다. 연속적인 "NAK 메시지"가 너무 많이 발생하면 긴급 절차가 수행됩니다.

- 참고 2 - 위의 각 그림\(화살표\)에는 메시지 텍스트만 표시됩니다. 실제로 완전한 메시지\(리더, 표시, 패딩 등 포함\)가 이러한 링크를 통해 교환됩니다.

---
## **3.  IMPLEMENTATION IN GORDO**
---
## **3.1  Introduction to GORDO**

GORDO는 SDS Sigma 7에 구현된 시분할 시스템입니다. 우리 논문과 관련된 몇 가지 특성을 아래에 간략하게 설명합니다.

```text
   3.1.1  GORDO file system
```

파일 시스템은 페이지 지향적입니다. 파일과 디렉토리로 구성됩니다. 파일은 제목과 파일 본문을 구성하는 여러 페이지로 구성됩니다. 디렉토리는 파일이나 다른 디렉토리를 가리키는 여러 항목으로 구성됩니다.

```text
   3.1.2  GORDO process
```

\* 프로세스는 프로그램\(프로시저 및 데이터\)에 논리 환경을 더한 것입니다. 즉, 프로세스는 GORDO 스케줄러에 의해 알려지고 제어되는 프로그램입니다.

\* 사용자\(작업\)는 다음과 같이 서로 다른 여러 프로세스를 가질 수 있습니다.

- 컴파일러, 로더, 에디터, 응용 프로그램 등 시스템 호출\(FORK\)을 통해 프로세스가 생성됩니다.

\* 프로세스가 참조할 수 있는 공간은 128k 워드 길이의 가상 공간이다. 그 중 일부\(8k\)는 운영 체제용으로 예약되어 있고, 다른 부분\(120k\)은 사용자가 직접 액세스합니다. 이는 나중에 '결합' 시 가상 공간의 일부를 채우거나 수정할 수 있습니다. \(아래 참조: 서비스 호출\) 다른 파일에서 가져온 페이지입니다. 그림 3은 이러한 결합을 보여줍니다.

\* 프로세스는 시스템 호출을 통해 서비스를 요청할 수 있습니다. 우리 논문과 관련된 시스템 호출은 다음과 같습니다.

WAKE: 수면 과정을 깨우기 위한\(활성화 설정\)

- 다른 프로세스\(또는 자체\)를 잠들게 하는 SLEEP 파일 공간의 페이지를 가상 공간에 연결하는 COUPLE.

\* 프로세스는 일반적으로 슬레이브 모드에서 실행됩니다. 그러나 I/O 프로세스로 설정되면 권한 있는 명령어에 액세스할 수 있습니다.

\* 프로세스는 "메일 박스" 디렉터리에 첨부된 파일을 통해 데이터를 공유할 수 있습니다.

비고: 이 노트에서는 프로세스와 프로그램이라는 단어가 같은 의미로 사용됩니다.

- \[그림 3 - 가상 공간과 결합 - PDF 파일 참조\]

---
## **3.2  Software Organization Overview**

그림 4는 전체 조직을 보여줍니다.

시스템은 "네트워크"와 "핸들러"라는 두 가지 주요 프로그램을 기반으로 합니다.

핸들러는 IMP-HOST 하드웨어 인터페이스와 밀접하게 관련된 I/O 인터럽트 루틴입니다. 수신 네트워크 메시지를 전송할 때 네트워크 프로세스를 제공합니다.

네트워크 프로세스는 대부분의 작업을 수행합니다.

주요 기능은 연결 열기/닫기 및 네트워크 메시지 전송/수신에 대한 사용자의 요청을 충족시키는 것입니다. 그렇게 하기 위해,

```text
   *  it establishes, identifies, and breaks the links upon using the
      allocation tables (HOST, CONNECT, INPUT LINK; see 3.3.1.1)

   *  it is aware of the presence of new users upon exploring the
      Network mail box directory;

   *  it communicates with active users by means of shared pages through
      which messages and requests are exchanged (connection shared
      pages);

   *  it formats incoming/outgoing messages in a working page.  This
      working page has an extension (emergency ring);
```

\* I/O 통신 버퍼를 포함하는 공유 페이지\(I/O 통신 페이지\)를 통해 핸들러와 통신합니다.

```text
        [Figure 4 - Software organization overview - see PDF file]
```

---
## **3.3  Software Description**
---
### **3.3.1  Data Structures**

```text
   3.3.1.1  Allocation tables: HOST, CONNECT, INPUT LINK
```

- 네트워크 프로그램은 3개의 테이블을 사용하여 링크와 연결을 설정, 식별 및 끊습니다.

```text
      A table sorted by remote HOST #.

      A table sorted by connection #.

      A table sorted by input link #.

        (a) HOST table (see figure 5)
```

- 무료로 나가는 링크를 나타내는 비트 테이블입니다. 다음과 같은 특징이 있습니다.

```text
            *  Location: Disc resident
```

- \* 결합: 네트워크 프로세스 가상 공간에 결합됩니다.

- \* 크기: 원격 HOST만큼의 슬롯 수.

- \* 슬롯 구조: 원격 HOST로 나가는 링크를 최대한 많은 비트, 즉 256.

```text
            *  Access: Indexing.  Each slot is accessed through a remote
                       HOST #.
```

- \* 특정 기능: 전체 테이블에서 64비트 이상을 켤 수 없습니다. 이 수치는 한 번에 활성화될 수 있는 최대 나가는 링크 수에 해당합니다\(원격 호스트 수에 관계 없음\).

```text
        (b)  CONNECT table
```

- 이 테이블은 모든 연결 환경을 추적합니다.

- 다음과 같은 특징을 가지고 있습니다.

```text
            *  Location:  Disc resident
```

- \* 결합: 네트워크 프로세스 가상 공간에 결합

- \* 크기: 사용 중인 연결만큼의 슬롯 수.

- \* 슬롯 구조: 그림 6 참조. 각 슬롯은 2워드 길이입니다.

- \* 접속 : 인덱싱. 각 슬롯은 연결 #을 통해 액세스됩니다. 처리 방법은 3.4를 참조하세요.

- \*특징 1: 기본 연결에 해당하는 슬롯 구조는 보조 연결의 슬롯 구조와 동일하지 않습니다\(그림 7 참조\). 이는 사용자 식별 및 요청이 기본 공유 페이지를 통해 수행되기 때문입니다.

```text
            *  Specific feature 2:  This table is handled in parallel
                                    with the connection pages (See 3.3.2
                                    (b))
```

- \*특징 3: 이 테이블은 주로 메시지 전송에 사용됩니다. \(각 연결에 대해 나가는 링크 # 및 원격 HOST #, 즉 메시지 전송에 필요한 모든 정보가 포함됩니다.\)

```text
        (c)  INPUT LINK table
```

- 이 테이블은 들어오는\(입력\) 링크를 모두 추적하므로 CONNECT 테이블과 밀접하게 관련되어 있습니다.

```text
                  [Figure 5 - HOST table - see PDF file]

         [Figure 6 - CONNECT table: Slot structure - see PDF file]

       [Figure 7 - INSERT LINK table: Slot structure - see PDF file]
```

다음과 같은 특징이 있습니다.

```text
   *  Location:  Disc resident.
```

\* 결합: 네트워크 프로세스 가상 공간에 결합됩니다.

\* 크기: 들어오는 링크만큼의 슬롯 수, 즉

- 연결

- \* 슬롯 구조: 그림 7 참조. 각 슬롯은 1워드 길이입니다.

```text
            *  Access:  Hashing.  The hashed key value is mainly based
                        upon the incoming link # and the remote HOST #.
```

\*특징 1: 이 테이블은 다음 용도로도 사용됩니다.

- 다음 연결을 설정하는 동안 연결 번호를 일시적으로 기억합니다. 처리 방법은 3.4를 참조하세요.

```text
            *  Specific feature 2:  This table is primarily used upon
                                    receiving messages.  (For each
                                    incoming link it contains the
                                    corresponding connection #, i.e.,
                                    indirectly the user identification
                                    to which the message should be
                                    passed along)

      3.3.1.2  Buffer pages
```

- 이제 설명할 모든 페이지에는 두 개의 버퍼\(입력 및 출력\)가 포함되어 있습니다. 이러한 버퍼는 메시지를 전달하거나 처리하는 데 사용됩니다.

- 각 버퍼의 크기는 최소한 메시지 크기와 동일해야 합니다\(예: 8095비트\). 우리는 두 버퍼가 모두 한 페이지\(512워드\) 내에 포함되도록 253워드\(8096비트\)의 버퍼 크기를 선택했습니다. 페이지의 나머지 6개 단어는 일반적으로 제어에 사용됩니다.

- 일반적인 버퍼 페이지 구조는 그림 8에 나와 있습니다.

```text
      (a)  I/O communication page

         See figure 9.
```

- 이 I/O 통신 페이지는 Handler와 Network 프로그램 간의 인터페이스로 사용됩니다.

- 이 페이지의 버퍼에서 메시지는 핸들러에 의해 단어 단위로 어셈블\(입력\)되거나 분해\(출력\)됩니다. 예를 들어 출력 버퍼의 네트워크 프로그램에 의해 정렬된 "ready to go" 메시지가 배송됩니다. 핸들러가 한 단어씩 출력합니다.

```text
         Main characteristics:
```

\* 위치: 핵심 상주: 잠긴 페이지

- \* 커플링: 네트워크 프로세스 가상 공간에 결합 \* 내용: \* 수신 메시지용 입력 버퍼\(253워드\) 발신 메시지용 출력 버퍼\(253워드\) \* 입력 제어 영역\(6 하프 워드\) \* 출력 제어 영역\(6 하프 워드\) \) \* 구조: 그림 9 참조. \* 특정 기능: \* 입력 버퍼는 핸들러\(하드웨어에서 읽음\)에 의해 채워지고 네트워크 프로그램에 의해 비워집니다. \* 출력 버퍼의 경우 그 반대

```text
      (b)  Connection shared pages (User-Network shared zone)

         General features:
```

- \* 연결 수만큼 공유 페이지가 있습니다.

\* 네트워크와 사용자 간에 공유되는 페이지입니다.

- 프로세스는 \(1\) 통과를 위한 통신 영역을 구성합니다.

- 메시지를 주고받고 \(2\) 제어 정보를 교환합니다\(예: 새로운 연결 설정 요청\).

```text
         Main characteristics:
```

\* 위치 : 디스크 상주

- \* 결합: 사용자 프로세스 가상 공간과 네트워크 프로세스 가상 공간 모두에 결합됩니다. \* 내용: - 수신 메시지용 입력 버퍼\(253워드\) - 발신 메시지용 출력 버퍼\(253워드\) - 입력 제어 영역\(6 하프 워드\) - 출력 제어 영역\(6 하프 워드\) \* 구조: 그림 10 참조. \* 특정 특징 1: - 입력 버퍼는 네트워크에 의해 채워지고 사용자에 의해 비워집니다. - 출력 버퍼의 경우도 마찬가지입니다. \*특징 2: 기본 연결 공유 페이지에 해당하는 제어 영역은 보조 연결의 제어 영역과 다릅니다. 이는 보조 연결 설정 요청이 네트워크 프로세스로 전송되는 것이 "1차 연결 제어 영역"을 통해 이루어지기 때문입니다.

```text
      (c)  Working page

         General feature:
```

- \* 이 페이지에서는 네트워크 및 처리기 프로그램이 서로 다른 메시지에 대해 독립적으로 작동할 수 있으므로 중복이 발생합니다. 예를 들어 핸들러가 하드웨어에 메시지를 전송하는 중일 때 네트워크 프로그램은 재설정 메시지를 포맷\(리더, 표시 등\)하여 발송할 수 있으므로 핸들러가 사용 가능해지자마자 다시 시작할 수 있습니다.

```text
         Main characteristics:
```

\* 위치 : 디스크 상주

- \* 결합: 네트워크 프로세스 가상 공간에 결합 \* 내용: - 들어오는 메시지에 대한 입력 버퍼\(253 워드\) - 나가는 메시지에 대한 출력 버퍼\(253 워드\)

```text
         Remark:
```

- 수신 중에 사용자 프로그램이 새 메시지를 수락할 준비가 되지 않은 경우가 발생할 수 있습니다. 이 경우 시스템의 혼잡을 방지하기 위해 네트워크는 들어오는 메시지를 긴급 링의 버퍼 중 하나에 일시적으로 저장합니다. \(이 링이 가득 차면 도움말 루틴이 호출됩니다.\)

- 방출 중에 모든 작업은 RFNM과 동기화되므로 이러한 절차를 제공할 필요가 없습니다. \(네트워크 프로그램에서는 이전에 전송한 메시지의 RFNM을 수신한 경우에만 사용자가 다시 전송하도록 허용합니다.\)

```text
             [Figure 8 - Typical buffer page - see PDF file]

       [Figure 9 - I/O Communication page structure - see PDF file]

       [Figure 10 - Connection shared page structure - see PDF file]
```

---
### **3.3.2  Programs**

```text
   3.3.2.1  Handler program

      General features:
```

- 메시지를 전송하거나 수신하기 위해 IMP/HOST 하드웨어 인터페이스를 구동하는 I/O 인터럽트 루틴입니다. 전송 및 수신은 전이중 모드로 수행됩니다.

```text
      Main characteristics:
```

- \* 위치 : 핵심 거주자. 핸들러는 운영 체제와 동일한 메모리 영역에 있으며 운영 체제의 일부로 간주될 수 있습니다.

- \* 시작: IMP-HOST 하드웨어 인터럽트에 의해. 이 인터럽트는 다음 중 하나에서 트리거됩니다.

- \* 전송 중 메시지 단어가 IMP로 완전히 전송된 경우

- \* 수신 중 IMP로부터 메시지 단어가 완전히 수신되었을 때

- \* 하드웨어가 Sigma 7 CPU로부터 '입력 시작' 또는 '출력 시작' 명령을 수신한 유휴 시간 동안. 이러한 명령은 인터럽트를 다시 유발하기 위해 네트워크 프로그램에 의해 발행됩니다.

- \(결과적으로 핸들러를 간접적으로 시작하기 위해\)

- \* 주요 기능: \* 내용\(IMP로 나가는 메시지\)을 전송할 때 출력 버퍼를 비웁니다. 이 작업은 단어 단위\(32비트\)로 수행되며 HOST-IMP 하드웨어를 구동하기 위해 "쓰기" 명령을 사용합니다.

- \* HOST-IMP 하드웨어\(수신 메시지\)로부터 수신된 데이터로 입력 버퍼를 채웁니다. 이 작업은 단어별로 수행되며 HOST-IMP 하드웨어를 구동하기 위해 "읽기" 명령을 사용합니다.

- \* 이전 작업이 완료되면 네트워크 프로그램을 깨웁니다.

```text
   3.3.2.2  Network program

      General features:
```

- 이 프로그램은 사용자에게 연결 열기/닫기 및 메시지 전송/수신 기능을 제공합니다. 하드웨어와의 인터페이스를 위한 보조 수단으로 핸들러를 사용합니다.

- GORDO의 관점에서는 이는 일반적인 프로세스이며 그렇게 취급됩니다.

```text
      Main characteristics:
```

- \* 위치 : 디스크 상주. 보다 정확하게는 잠자기 상태일 때 디스크에 있고 프로그램에 의해 깨어날 때 코어에서 호출됩니다. \* 개시\(Initiation\): 사용자 프로세스나 핸들러에 의해 발행된 'WAKE' 서비스 호출을 통해 시작됩니다. \* 주요 기능: \* 사용자의 요청에 따라 나가는 연결을 설정/삭제합니다. 그렇게 하기 위해 링크를 설정/해제하기 위해 원격 호스트에 제어 메시지\(2.4.2 참조\)를 보냅니다. 그런 다음 사용자에게 다시 알립니다. \* 예를 들어 연결 설정/삭제\(원격 호스트에서 요청한 메시지\)에 기여하기 위해 들어오는 제어 메시지\(제어 링크를 통해 전송됨\)의 처리를 보장합니다.

- \* 나가는 메시지 전송을 준비합니다. 공유 페이지에서 문자 메시지를 선택하고\(사용자가 메시지를 저장함\) 형식을 지정하고\(리더, 표시, 체크섬 추가 등\) 전송을 위해 핸들러에 전달합니다. \* 들어오는 메시지의 전달을 보장합니다. 위의 동작과 반대되는 동작입니다. 메시지가 전달되어야 하는 사용자는 리더를 통해 식별됩니다.

```text
      *  Virtual space configuration:  See figure 11.
```

- \* 특정 기능: I/O 프로세스로 통합되어 특권 명령어\(핸들러를 간접적으로 시작하기 위한 RD/WD\)에 액세스할 수 있습니다.

```text
        [Figure 11 - Network Process Virtual Space - see PDF file]
```

---
## **3.4  Software Procedures**

자세한 소프트웨어 절차는 부록 A에 첨부된 순서도에 나와 있습니다.

그러나 구현을 빠르게 이해하기 위해 몇 가지 일반적인 소프트웨어 절차를 아래에 나열합니다.

---
### **3.4.1  Description of some typical sequences**

사용자가 처리할 수 있는 일부 트랜잭션\(2.4 참조\)을 고려하고 그것이 암시하는 기본 소프트웨어 절차를 지적하십시오. 각 경우에 대해 \(i\) 사용자 프로그램이 수행하는 작업과 \(ii\) 네트워크 프로그램이 수행하는 작업을 설명합니다.

```text
   (a)  Open a primary link (See also 2.4.2)
```

- \(i\) 사용자 프로그램이 수행하는 작업\[1\]:

- \* 네트워크 메일 박스 디렉토리에 파일 이름\(예: DATA\)을 저장합니다. \* 이 파일의 첫 번째 페이지를 가상 공간에 연결합니다. \* 이 페이지에 정보를 저장합니다\(해당 작업/프로세스 #, 원격 HOST #, 예: \(i\)\). \* 네트워크 프로세스를 깨웁니다. \* 잠에 들어갑니다.

- \(ii\) 네트워크 프로그램의 기능:

- \* 네트워크 메일함 디렉토리를 탐색하고 DATA 파일에 액세스합니다. \* 이 파일의 첫 번째 페이지를 가상 공간\(공유 영역, 3.3.1.2 참조\)에 연결합니다. 이 페이지가 공유 영역에서 k번째 페이지라고 가정합니다. k는 내부 연결 #입니다. \* 새로운 HOST 테이블의 i번째 슬롯을 탐색하고\(3.3.1.1\(a\) 참조\) 첫 번째 비트 = 0, 예를 들어 \(알파\)번째 비트를 선택합니다. alpha는 나가는 링크 #에 해당합니다. \* CONNECT 테이블의 k번째 슬롯에 정보\(작업/프로세스 번호, 원격 HOST #\(i\), 나가는 링크 번호\(알파\)\)를 저장한다\(3.3.1.2 참조\). \* INPUT LINK 테이블에 연결 #\(k\)을 일시적으로 저장합니다. 이는 이 테이블에 항목을 생성할 때 수행됩니다\(키 값 해싱: "나가는 링크 #\(알파\) + 원격 HOST #\(i\) + 나가는 플래그".\). \* 메시지 텍스트 ENQ PRIM 0 0 a를 준비하고 리더 추가, 표시, 체크섬 등을 통해 완전한 메시지 형식을 지정합니다. \* 핸들러 상태\(I/O 잠긴 페이지의 비트\)를 확인합니다. 핸들러가 사용 가능하면 I/O 잠긴 페이지의 출력 버퍼에 '준비 완료' 제어 메시지를 저장하고 핸들러를 시작한 다음 절전 모드로 전환됩니다. 그렇지 않으면 잠들게 됩니다.

잠시 후 핸들러는 완전한 메시지를 수신했기 때문에 네트워크 프로세스를 깨웁니다. 이 메시지는 연결 설정을 승인하기 위해 원격 HOST에서 보낸 제어 메시지라고 가정합니다. 메시지 텍스트는 다음과 같아야 합니다.

```text
            ACK ENQ PRIM 0 0 alpha 0 0 beta

   where beta is the incoming link #.  (See 2.4.2)
```

이제 위의 제어 메시지를 수신할 때 네트워크 프로그램이 수행하는 작업을 살펴보겠습니다.

```text
              *  it retrieves the connection # previously stored in the
                 INPUT LINK table upon re-hashing the same key value
                 (See above).  Also it deletes this entry;
              *  it creates an entry in the INPUT LINK table for the
                 incoming link.  For so doing it hashes the key value:
                 "incoming link # (beta]) + remote HOST # (i) +
                 "incoming flag".  In this entry it stores the HOST #
                 (i), the incoming link # (beta), and connection # (k);
```

- \* 들어오는 링크 #\(베타\)을 저장할 때 CONNECT 테이블의 k번째 슬롯을 업데이트합니다. \* k번째 공유 페이지\(방금 열린 기본 연결에 해당하는 페이지\)에서 'net-user' 비트를 켜고 사용자 프로세스를 깨웁니다. \* 잠에 들어갑니다.

\(b\) 기본 링크를 통해 메시지 전송

- \(i\) 사용자 프로그램이 하는 일\[1\].

- \* 기본 연결 공유 페이지의 출력 버퍼에 메시지 텍스트를 저장합니다\(3.3.1.2 참조\). \* 이 페이지의 'user-net' 비트를 켜고 네트워크 프로세스를 깨웁니다. \* 잠에 들어갑니다.

- \(ii\) 네트워크 프로그램의 기능:

- \* 사용자 요청을 찾습니다. 즉, 연결 공유 페이지를 순서대로 탐색하고 'user-net' 비트가 켜져 있는 페이지를 선택합니다. k가 공유 목록에서 선택된 페이지 #이고 K가 연결 #이라고 가정합니다. \* 공유 페이지 k의 '요청 비트'를 테스트하여 요청 유형을 결정합니다. 메시지 전송을 위한 요청임을 알게 됩니다. \* 공유 페이지 k의 출력 버퍼에서 메시지 텍스트를 가져와 이를 완전한 메시지로 형식화하고 위와 매우 유사한 방식으로 핸들러에 전송합니다\(기본 링크 열기 참조\). \* 잠에 들어갑니다.

- \[1\] 참고: 첫 번째 단계에서는 사용자가 자신의 프로그램에 네트워크 기능을 직접 작성합니다. 나중에 서브루틴을 사용자가 마음대로 사용할 수 있게 됩니다. 이러한 서브루틴은 2.4에 설명된 것과 매우 유사합니다.

---
# **APPENDIX A**

```text
   Flowcharts
```

- \[흐름도는 PDF 파일 참조\]

- \[ 이 RFC는 입력을 위해 기계 판독 가능한 형식으로 작성되었습니다. \] \[ Bob German이 99년 8월에 온라인 RFC 아카이브에 저장함 \]