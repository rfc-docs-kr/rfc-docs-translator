

```text
Network Working Group                                           4691
RFC-5                                                           Jeff Rulifson
                                                                June 2, l969

                                DEL
```

:DEL, 02/06/69 1010:58 JFR ; .DSN=1; .LSP=0; \['=\] 그리고 SP가 아님 ; \['?\];
이중 전송?

---
# **ABSTRACT**

DEL\(Decode-Encode Language\)은 두 가지 특정 컴퓨터 네트워크 작업에 맞게 조정된 기계 독립적 언어입니다.

- 대화형 콘솔에서 입력 코드를 받아들이고 즉각적인 피드백을 제공하며 결과 정보를 네트워크 전송을 위한 메시지 패킷으로 압축합니다.

- 다른 컴퓨터로부터 메시지 패킷을 받아들이고, 압축을 풀고, 표시 정보 트리를 구축하고, 대화형 스테이션에서 사용자에게 기타 정보를 보냅니다.

이것은 DEL 언어의 발전을 위한 작업 문서입니다. 의견은 SRI의 Jeff Rulifson을 통해 작성해야 합니다.

---
# **FORWARD**

초기 ARPA 네트워크 실무 그룹은 1968년 10월 25\~26일 SRI에서 만났습니다.

- 네트워크를 통한 대화형 프로그램의 실행이 직면하게 될 첫 번째 문제라는 것이 사전에 일반적으로 합의되었습니다.

- DEL과 유사한 접근 방식의 기본 개념에 대해 이미 동의한 이 그룹은 DEL 프로그램에 대한 몇 가지 용어, 기대 사항 및 제안된 의미 기능 목록을 설정합니다.

- 회의에는 Andrews, Baray, Carr, Crocker, Rulifson 및 Stoughton이 있었습니다.

이후 2차 회의가 단편적으로 열렸습니다.

- Crocker는 1968년 11월 18일 SRI에서 Rulifson을 만났습니다. 이로 인해 공식적인 공동 루틴이 통합되었습니다.

- 그리고 Stoughton은 1968년 12월 12일 SRI에서 Rulifson을 만났습니다. 1969년 1월 말에 아마도 UTAH에서 그룹으로 다시 만나기로 결정되었습니다.

이 논문의 첫 번째 공개 발표는 1969년 2월 13일 케임브리지에서 열린 BBN NET 회의에서였습니다.

---
# **NET STANDARD TRANSLATORS        **

NST NST 라이브러리는 수신한 DEL 프로그램에서 사용자 사이트에서 컴파일된 코드와 효율적으로 결합하는 데 필요한 프로그램 세트입니다. NET 대화형 시스템 통신에 대한 NST-DEL 접근 방식은 광범위한 스펙트럼에서 작동하도록 고안되었습니다.

NST-DEL 사용의 가장 낮은 수준은 사용자 프로그램이 사용자 호스트에서 수신하는 것과 동일한 형식의 정보인 서버 호스트로 직접 전송되는 것입니다.

- 이 모드에서는 NST가 기본적으로 비활성 상태로 설정됩니다. DEL 프로그램은 범용 하드웨어 표현 입력을 받지 않지만 사용자 호스트에 대한 일반적인 방식으로 입력을 받습니다.

- 그리고 DEL 1 프로그램은 단지 메시지 작성기 및 송신자가 됩니다.

NST-DEL의 중간 용도는 사용자 호스트에서 TTY에 대한 에코 테이블을 갖는 것입니다.

- 이 모드에서 DEL 프로그램은 사용자에 대해 전이중 TTY를 실행합니다.

- 문자를 에코하고, 이를 서버 호스트의 문자 세트로 변환하고, 변환된 문자를 메시지에 압축하고, 적절한 중단 문자에서 메시지를 보냅니다.

- 메시지가 서버 호스트에서 오면 DEL 프로그램은 이를 사용자 호스트 문자 집합으로 변환하여 TTY에 인쇄합니다.

DEL의 더 야심 찬 작업은 NET을 통해 원격 콘솔에서 대규모 디스플레이 지향 시스템을 작동하는 것입니다.

- 대규모 대화형 시스템은 일반적으로 사용자에게 많은 피드백을 제공합니다. 피드백의 특이한 특성으로 인해 에코 테이블로 모델링하는 것이 불가능하므로 버튼 상태가 변경될 때마다 TSS에서 사용자 프로그램이 활성화되어야 합니다.

- 이로 인해 TSS에 불필요하게 큰 로드가 발생하며, 시스템이 NET을 통해 실행되는 경우 두 개의 시스템을 쉽게 로드할 수 있습니다.

- TSS의 이중 오버로드를 방지하기 위해 DEL 프로그램이 사용자 호스트에서 실행됩니다. 복잡한 에코 테이블처럼 모든 즉각적인 피드백을 처리합니다. 적절한 버튼을 누르면 메시지가 서버 호스트로 전송되고 그 대가로 디스플레이 업데이트가 수신됩니다.

- 더 어렵고 종종 무시되는 문제 중 하나는 하나의 비표준 콘솔을 다른 비표준 콘솔에서 효과적으로 시뮬레이션하는 것입니다.

- 우리는 DEL 프로그램의 코루틴 구조를 통해 이 문제를 해결할 수 있는 수단을 제공하려고 합니다. 복잡한 대화형 시스템의 경우 DEL 프로그램의 일부는 서버-호스트 프로그래머가 구성합니다. 이 프로그램과 입력 스트림 사이의 인터페이스는 프로그래머가 사용자 호스트 사이트에서 쉽게 삽입할 수 있습니다.

---
# **UNIVERSAL HARDWARE REPRESENTATION**

시설의 사용자 코드를 다른 시설에 매핑하는 데 필요한 변환기 수를 최소화하기 위해 범용 하드웨어 표현이 있습니다.

이것은 단순히 초기 네트워크의 모든 대화형 디스플레이 스테이션에 있는 모든 하드웨어 장치에 대해 일반적인 용어로 말하는 방법입니다.

예를 들어, 디스플레이는 정사각형으로 간주되며 중간점은 좌표\(0.0\)를 가지며 범위는 두 축에서 -1\~1입니다. 이제 디스플레이의 특정 래스터 점 밀도 수에 관계없이 점을 원하는 정확도로 지정할 수 있습니다.

표현은 DEL의 형식적 설명과 함께 제공되는 의미론적 설명에서 논의됩니다.

---
# **INTRODUCTION TO THE NETWORK STANDARD TRANSLATOR (NST)**

Utah와 같은 원격 사이트의 사용자가 AHI 시스템에 입력되어 NLS를 실행하려고 한다고 가정합니다.

첫 번째 단계는 일반적인 방법으로 NLS를 입력하는 것입니다. 그 때 유타 시스템은 NLS에 기호 프로그램을 요청할 것입니다.

- REP 이 프로그램은 DEL로 작성되었습니다. 이를 NLS 원격 인코딩 프로그램\(REP\)이라고 합니다.

프로그램은 범용 하드웨어의 입력을 받아들입니다.

- NLS에서 사용할 수 있는 형태로 표현하고 번역합니다.

버퍼에 문자를 넣을 수도 있고 일부 로컬 작업도 수행할 수 있습니다.

-  피드백.

프로그램이 유타에서 처음 수신되면 표준 라이브러리와 함께 실행되도록 컴파일되고 로드됩니다.

Utah 콘솔의 모든 입력은 먼저 NLS NEP로 이동합니다. 처리, 분석, 차단, 번역 등이 수행됩니다. NEP가 해당 상태에 적합한 문자를 수신하면 최종적으로 940으로의 전송을 시작할 수 있습니다. 전송된 비트는 940에서 허용되는 형식이며 아마도 표준 형식일 수 있습니다. NLSW는 유타와 다른 NET 사용자를 구별할 필요가 없습니다.

---
# **ADVANTAGES OF NST**

각 노드가 NST의 라이브러리 부분을 구현한 후에는 각 하위 시스템에 대해 하나의 프로그램, 즉 NET 하드웨어 표현을 고유한 특수 비트 형식으로 매핑하는 각 사용자에게 보내는 기호 파일만 작성하면 됩니다.

이는 다음과 같은 경우에 기대할 수 있는 최소한의 프로그래밍입니다.

- 콘솔을 최대한 활용합니다.

- 인코딩 변환을 실행하는 NST는 사용자 사이트에서 코딩되므로 콘솔의 하드웨어를 최대한 활용할 수 있습니다. 또한 호스트에서 새 변환 테이블이나 다른 변환 테이블을 요구하지 않고도 하드웨어 기능을 추가하거나 제거할 수 있습니다.

- 로컬 사용자는 호스트 사이트에서 제공되는 시스템의 변경 사항에 대한 최신 정보도 유지됩니다. 새로운 기능이 추가되면 호스트 프로그래머는 기호 인코딩 프로그램을 변경합니다. 이 새로운 프로그램이 컴파일되어 사용자 사이트에서 사용되면 새로운 기능이 자동으로 포함됩니다.

인코딩 변환 프로그램을 기호적으로 전송하면 이점이 분명해집니다.

- 각 사이트는 적합하다고 판단되는 방식으로 번역할 수 있습니다. 따라서 각 사이트의 기계 코드는 해당 사이트에 맞게 생성될 수 있습니다. 결과적으로 실행 시간이 빨라지고 코드 밀도가 높아집니다.

- 또한 사용자 사이트에서 코딩된 추가 기호 프로그램은 사용자 모니터 시스템과 호스트 시스템의 DEL 프로그램 간에 쉽게 인터페이스될 수 있습니다. 이는 인간-기계 상호 작용에 필요한 유연성을 잃지 않으면서 콘솔 확장 문제\(예: 특이한 키 및 버튼 수용\)를 완화해야 합니다.

```text
   It is expected that when there is matching hardware, the symbolic
   programs will take this into account and avoid any unnecessary
   computing.  This is immediately possible through the code
   translation constructs of DEL.  It may someday be possible through
   program composition (when Crocker tells us how??)
```

---
# **AHI NLS - USER CONSOLE COMMUNICATION - AN EXAMPLE**

```text
   BLOCK DIAGRAM
```

- 그림의 오른쪽은 사용자의 메인 컴퓨터에서 수행되는 기능을 나타냅니다. 왼쪽은 호스트 컴퓨터에서 수행된 작업을 나타냅니다.

- 그림의 각 라벨은 동일한 이름을 가진 진술에 해당합니다.

- 이 사진에는 4개의 트레일이 연결되어 있습니다. 첫 번째 링크는 \(순방향으로\) 네트워크 정보에만 관련된 레이블입니다. 두 번째는 전체 정보 흐름을 연결합니다\(다시 정방향으로\). 마지막 두 개는 처음 두 개와 동일하지만 반대 방향입니다. 이들은 각각 포인터 t1부터 t4까지 설정될 수 있습니다.

```text
         [">tif:] OR I" >nif"]; ["<tif:] OR ["<nif"];
```

---
# **USER-TO-HOST TRANSMISSION**

키보드는 사용자 콘솔에 있는 입력 장치 세트입니다. 모니터 및 인터럽트 처리기 수준을 통과한 후 스테이션의 입력 비트는 결국 인코딩 변환기로 전달됩니다. \[\>nif\(인코딩\)\]

인코딩은 입력을 처리할 제공 호스트 하위 시스템에 적합한 형식으로 반 원시 입력 비트를 입력 스트림에 매핑합니다. \[\>nif\(hrt\)<nif\(키보드\)\]

- 서브시스템이 처음 요청되었을 때 서버-호스트 서브시스템에서 인코딩 프로그램을 제공했습니다. 이는 기호 형식으로 사용자 시스템에 전송되며 사용자 시스템에서 해당 시스템에 특히 적합한 코드로 컴파일됩니다.

- 문자를 분리하고, 여러 문자를 단일 문자로 매핑하거나 그 반대로 매핑하고, 문자를 번역하고, 사용자에게 즉각적인 피드백을 제공하기 위해 팩할 수 있습니다.

1 dm 인코딩 변환기의 즉각적인 피드백은 먼저 로컬 디스플레이 관리로 이동하여 NET 표준에서 로컬 디스플레이 하드웨어로 매핑됩니다.

인코딩에서 광범위한 에코 출력이 나올 수 있습니다.

- 번역가. 간단한 문자 반향은 최소화되는 반면 명령 및 시스템 상태 피드백은 일반적입니다.

- 서버-호스트 사용자 스테이션에서도 이루어지지 않는 제어 및 피드백 기능이 로컬 디스플레이 제어에서 이루어지길 기대하는 것이 합리적이다. 예를 들어, 고속 디스플레이를 사용하는 사람들은 저장 튜브에서는 불가능한 기능인 Culler 디스플레이의 곡선을 선택적으로 지우기를 원할 수 있습니다.

서버-호스트에 대한 인코딩 변환기의 출력은 보이지 않는 IMP로 이동하고, 적절한 크기로 분할되고 인코딩 변환기에 의해 레이블이 지정된 다음 NET-호스트 변환기로 이동합니다.

- 사용자로부터의 출력은 온라인 입력보다 많을 수 있습니다. 이는 컴퓨터에서 생성된 데이터 또는 서버 호스트 사이트에서만 생성 및 사용되지만 사용자 호스트 사이트에 저장되는 파일과 같은 더 큰 항목일 수 있습니다.

- 이러한 종류의 정보는 이미 서버-호스트 형식인 경우 번역을 피할 수 있으며, 데이터 블록인 경우 또 다른 종류의 번역을 거칠 수 있습니다.

hrp 마침내 호스트에 도달한 다음 호스트 수신 프로그램을 거쳐야 합니다. 이는 인코딩 프로그램이 전송한 표준 전송 스타일 비트 패킷을 호스트가 수용할 수 있는 메시지로 매핑하고 재정렬합니다. 이 프로그램은 호스트 시스템 모니터의 일부일 수도 있습니다. \[\>tif\(넷 모드\)<nif\(코드\)\]

---
# **HOST-TO-USER TRANSMISSION**

decode 서버-호스트의 출력은 처음에 인코딩 맵과 유사하고 아마도 더 복잡한 변환 맵인 디코드를 거칩니다. \[\>nif\(urt\)\>tif\(imp ctrl\)<tif\(net 모드\)\]

- 이 맵은 최소한 디스플레이 출력을 단순화된 논리 엔터티 출력 스트림으로 형식화하며, 그 중 의미 있는 부분은 사용자 사이트에서 다양한 방식으로 처리될 수 있습니다.

- 인코딩 프로그램이 사용자 컴퓨터로 전송됨과 동시에 디코드 프로그램이 호스트 컴퓨터로 전송되었습니다. 프로그램은 처음에 기호 형식으로 되어 있으며 호스트 시스템에서 효율적으로 실행되도록 컴파일됩니다. 사용자 사이트에서 다양한 줄 너비를 처리할 수 있도록 문자 줄을 논리적으로 식별해야 합니다.

- 어떤 형태의 논리적 라인 식별도 이루어져야 합니다. 예를 들어, 디스플레이에 직선을 그리려면 일련의 500개의 짧은 벡터가 아니라 이 사실을 전송해야 합니다.

- 상황이 안정됨에 따라 점점 더 복잡한 구조적 디스플레이 정보\(LEAP 방식\)가 사용자 사이트로 전송되고 수용되어 실시간 디스플레이 조작에 대한 책임이 사용자에게 더 가까워질 수 있습니다.

imp ctrl 서버 호스트가 제어를 보내려고 할 수도 있습니다.

- IMP에 대한 정보. 이 정보의 형식화는 호스트 디코더에 의해 수행됩니다. \[\>tif\(urt\) <tif\(디코드\)\]

- 호스트 디코더가 제공하는 다른 제어 정보는 메시지 분할 및 식별이므로 사용자 사이트에서 적절한 조립 및 정렬이 수행될 수 있습니다.

호스트 디코더에서 정보는 보이지 않는 IMP로 전달되고 NET에서 사용자로의 변환기로 직접 전달됩니다. 메시지에 대해 수행되는 유일한 작업은 메시지를 섞는 것뿐입니다.

urt 사용자 수신 변환기는 사용자 사이트 IMP 1에서 메시지를 수락하고 사용자 사이트 표시를 위해 이를 수정합니다. \[\>nif\(d ctrl\)\>tif\(prgm ctrl\)<tif\(imp ctrl\)<nif\(디코드\)\]

- 최소한의 작업은 메시지 조각을 재정렬하는 것입니다. dctrl 그러나 디스플레이 출력의 경우 더 많은 작업이 필요합니다. NET 논리적 표시 정보는 사용자 사이트 형식으로 넣어야 합니다. 디스플레이 제어가 이 작업을 수행합니다. \(인코딩\)과 \(디코딩\) 사이를 조정하므로 사용자 사이트에 로컬 디스플레이 관리 기능을 제공할 수 있습니다. \[\>nif\(디스플레이\)<nif\(urt\)\]

- prgmctrl 또 다른 작업은 특정 사용자 사이트 하위 시스템으로 정보를 선택적으로 변환하고 라우팅하는 것입니다. \[\>tif\(dctrl\)<tif\(urt\)\]

- 예를 들어, 부동 소수점 정보 블록은 사용자 스타일 단어로 변환되어 처리 또는 저장을 위해 블록 형식으로 하위 시스템으로 전송될 수 있습니다.

- 이 정보의 스타일과 번역은 인쇄된 이미지 중심 형식이 아니라 빠른 번역에 적합한 컴팩트 바이너리 형식일 수 있습니다.

- \(표시\)는 사용자에게 출력됩니다. \[<nif\(d Ctrl\)\]

```text
   
   USER-TO-HOST INDIRECT TRANSMISSION
```

- \(net 모드\) 원격 사용자가 다른 노드를 통해 간접적으로 해당 노드에 연결할 수 있는 모드입니다. \[<nif\(디코드\)<tif\(hrt\)\]

---
# **DEL SYNTAX**

NLS 사용자를 위한 참고 사항 컴파일러의 일부가 아닌 이 분기의 모든 명령문은 마침표로 끝나야 합니다.

- DEL 컴파일러를 컴파일하려면:

- 콘텐츠 분석기\(위쪽 화살표 기호\)P1 SE\(P1\) <-"-;\)에 대해 이 패턴을 설정합니다. 포인터 "del"은 패턴의 첫 번째 문자에 있습니다.

- 컴파일러의 첫 번째 문장으로 점프합니다. 이 명령문에는 포인터 "c"가 있습니다.

```text
         And output the compiler to file  ( '/A-DEL' ).  The pointer "f"
         is on the name of the file for the compiler output -

   PROGRAMS

      SYNTAX

         -meta file (k=100.m=300,n=20,s=900)

         file = mesdecl $declaration $procedure "FINISH";

         procedure =

           procname (

              (

                 type "FUNCTION" /

                 "PROCEDURE" ) .id (type .id / -empty)) /

              "CO-ROUTINE") ' /

           $declaration labeledst $(labeledst ';) "endp.";

         labeledst = ((left arrow symbol).id ': / .empty) statement;

         type = "INTEGER" / "REAL" ;

         procname = .id;
```

- 컴파일러가 더 나은 코드 생성 및 런타임 검사를 할 수 있도록 함수를 프로시저와 차별화합니다.

```text
         Functions return values.

         Procedures do not return values.
```

- 코루틴에는 이름이나 인수가 없습니다. 초기 호출 지점에는 파이프 선언이 제공됩니다.

- 전역 선언이 어떻게 될지는 명확하지 않습니다.

---
# **DECLARATIONS**

```text
   SYNTAX

      declaration = numbertype / structuredtype / label / lcl2uhr /
      uhr2rmt / pipetype;

      numbertype = : ("REAL" / "INTEGER") ("CONSTANT" conlist /
      varlist);

      conlist =

         .id '(left arrow symbol)constant

         $('. .id '(left arrow symbol)constant);

      varlist =

         .id ('(left arrow symbol)constant / .empty)

         $('. .id('(left arrow symbol)constant / .empty));

      idlist = .id $('. .id);

      structuredtype = (tree" / "pointer" / "buffer" ) idlist;

      label = "LABEL1" idlist;

      pipetype = PIPE" pairedids $(', pairedids);

      pairedids = .id .id;

      procname = .id;

      integerv = .id;

      pipename = .id;

      labelv = .id;
```

상수로 선언된 변수는 런타임 시 읽기 전용 메모리에 저장될 수 있습니다.

라벨 선언은 프로그램에서 라벨의 기계 주소를 값으로 포함할 수 있는 셀을 선언하는 것입니다. 이는 B5500 라벨 선언이 아닙니다.

파이프 선언에서 각 쌍의 첫 번째 .ID는 파이프 이름이고 두 번째는 파이프의 초기 시작 지점입니다.

---
# **ARITHMETIC**

```text
   SYNTAX

      exp = "IF" conjunct "THEN" exp "ELSE" exp;

      sum = term (

         '+ sum /

         '- sum /

         -empty);

      term = factor (

         '* term /

         '/ term /

         '(up arrow symbol) term /

         .empty);

      factor = '- factor / bitop;

      bitop = compliment (

         '/' bitop /

         '/'\ bitop /

         '& bitop / (

         .empty);

      compliment = "--" primary / primary;
```

\(위쪽 화살표 기호\)는 모드를 의미합니다. /\는 배타적 또는을 의미합니다.

단항 마이너스가 허용되며 x\*-y를 쓸 수 있도록 구문 분석됩니다.

비트 연산자에는 표준 규칙이 없으므로 모두 동일한 우선 순위를 가지며 그룹화에는 괄호를 사용해야 합니다.

칭찬은 l의 칭찬입니다.

모든 산술 및 비트 연산은 코드를 실행하는 시스템의 모드와 스타일에서 발생한다고 가정합니다. 단어 길이, 2의 칭찬 연산 등을 활용하는 사람은 결국 문제를 겪게 됩니다.

---
# **PRIMARY**

```text
   SYNTAX

      primary =

         constant /

         builtin /

         variable / (

         block /

         '( exp ');

      variable = .id (

         '(symbol for left arrow) exp /

         '( block ') /

         .empty);

      constant =  integer / real / string;

      builtin =

         mesinfo /

         cortnin /

         ("MIN" / "MAX") exp $('. exp) '/ ;
```

괄호 안에 있는 표현식은 일련의 표현식일 수 있습니다. 계열의 값은 런타임에 마지막으로 실행된 계열의 값입니다.

서브루틴에는 이름 인수로 한 번의 호출이 있을 수 있습니다.

```text
   Expressions may be mixed.  Strings are a big problem?  Rulifson
   also wants to get rid of real numbers!!
```

---
# **CONJUNCTIVE EXPRESSION**

```text
   SYNTAX

      conjunct = disjunct ("AND" conjunct / .empty);

      disjunct = negation ("OR" negation / .empty);

      negation = "NOT" relation / relation;

      relation =

         '( conjunct ') /

         sum (

           "<=" sum /

           ">=" sum /

           '< sum /

           '> sum /

           '= sum /

           '" sum /

           .empty);
```

결합 구문은 합계가 아닌 결합이 값을 가질 필요가 없고 코드에서 점프를 사용하여 평가될 수 있는 방식으로 조작됩니다. 접속사에 대한 참조는 논리적 결정이 필요한 위치\(예: if 및 while 문\)에서만 이루어집니다.

우리는 대부분의 컴파일러가 런타임 시 불필요한 평가를 건너뛸 만큼 똑똑해지기를 바랍니다. 즉, 왼쪽 부분이 거짓인 결합 또는 왼쪽 부분이 참인 결합은 해당 오른쪽 부분을 평가할 필요가 없습니다.

---
# **ARITHMETIC EXPRESSION**

```text
   SYNTAX

      statement = conditional / unconditional;

      unconditional = loopst / cases / cibtrikst / uist / treest /
      block / null / exp;

      conditional = "IF" conjunct "THEN" unconditional (

         "ELSE" conditional /

         .empty);

      block = "begin" exp $('; exp) "end";
```

표현식은 명령문일 수 있습니다. 조건문에서 else 부분은 선택 사항이지만 표현식에서는 필수입니다. 이는 구문 규칙의 왼쪽 부분이 정렬되는 방식의 부작용입니다.

---
# **SEMI-TREE MANIPULATION AND TESTING**

```text
   SYNTAX

      treest = setpntr / insertpntr / deletepntr;

      setpntr = "set" "pointer" pntrname "to" pntrexp;

      pntrexp = direction pntrexp / pntrname;

      insertpntr = "insert" pntrexp "as"

         (("left" / "right") "brother") /

         (("first" / "last: ) "daughter") "of" pntrexp;

      direction =

         "up" /

         "down" /

         "forward" /

         "backward: /

         "head" /

         "tail";

      plantree = "replace" pntrname "with" pntrexp;

      deletepntr = "delete: pntrname;

      tree = '( tree1 ') ;

      tree1 = nodename $nodename ;

      nodename = terminal / '( tree1 ');

      terminal = treename / buffername / point ername;

      treename = id;

      treedecl = "pointer" .id / "tree" .id;
```

트리 작성 시 괄호를 추가하면 LISP에서와 마찬가지로 선형 하위 분류가 발생합니다.

---
# **FLOW AND CONTROL**

```text
   controlst = gost / subst / loopstr / casest;
```

명세서로 이동

```text
      gost = "GO" "TO" (labelv / .id);

         assignlabel = "ASSIGN" .id "TO" labelv;

   SUBROUTINES

      subst = callst / returnst / cortnout;

         callst = "CALL" procname (exp / .emptyu);

         returnst = "RETURN" (exp / .empty);

         cortnout = "STUFF" exp "IN" pipename;

      cortnin = "FETCH" pipename;
```

- FETCH는 명명된 코루틴을 호출하여 값이 계산되는 내장 함수입니다.

```text
   LOOP STATEMENTS

      SYNTAX

         loopst = whilest / untilst / forst;

         whilest = "WHILE" conjunct "DO" statement;

         untilst = "UNTIL" conjunct "DO" statement;

         forst = "FOR" integerv '- exp ("BY" exp / .empty) "TO" exp

         "DO" statements;
```

- while문과 Until문의 값은 각각 false와 true\(또는 0과 0이 아닌\)로 정의됩니다.

- For 문은 초기화 시 초기 exp를 부분적으로 평가하고 부분적으로 한 번만 평가합니다. for 문의 실행 중인 인덱스는 루프 내에서 변경할 수 없으며 읽기만 가능합니다. 만약 일부 컴파일러가 이를 더 잘 활용할 수 있다면\(예를 들어 레지스터에 넣음\) 더 좋습니다. 증분과 경계는 모두 초기화 중에 정수로 반올림됩니다.

---
# **CASE STATEMENTS**

```text
   SYNTAX

      casest = ithcasest / condcasest;

      ithcasest = "ITHCASE" exp "OF" "BEGIN" statement $(';
      statement) "END";

      condcasest = "CASE" exp "OF" "BEGIN" condcs $('; condcs)
      "OTHERWISE" statement "END";

      condcs = conjunct ': statement;
```

Case문의 값은 마지막으로 실행된 Case의 값입니다.

---
# **EXTRA STATEMENTS**

```text
   null = "NULL";
```

---
# **I/O STATEMENTS**

```text
   iost = messagest / dspyst ;

   MESSAGES

      SYNTAX

         messagest = buildmes / demand;

            buildmest = startmes / appendmes / sendmes;

              startmes = "start" "message";

              appendmes = "append" "message" "byute" exp;

              sendmes = "send" "message";

              
           demandmes = "demand" "Message";

      mesinfo =

         "get" "message" "byte"

         "message1" "length" /

         "message" empty: '?;

      mesdecl = "message" "bytes" "are" ,byn "bits" long" '..
```

---
# **DISPLAY BUFFERS**

```text
   SYNTAX

      dspyst = startbuffer / bufappend / estab;

      startbuffer - "start" "buffer";

      bufappend = "append" bufstuff $('& bufstuff);

      bufstuff = :

         "parameters" dspyparm $('. dspyparm) /

         "character" exp /

         "string"1 strilng /

         "vector" ("from" exp ':exp / .empty) "to" exp '. exp /

         "position" (onoff / .empty) "beam" "to" exp '= exp/

         curve" ;

      dspyparm F :

         "intensity" "to" exp /

         "character" "width" "to" exp /

         "blink" onoff /

        "italics" onff;

      onoff = "on" / "off";

      estab = "establish" buffername;

   LOGICAL SCREEN
```

화면은 정사각형으로 간주됩니다. 좌표는

- 두 축 모두에서 -1에서 +1까지 정규화되었습니다.

화면과 연결된 위치 레지스터는 다음과 같습니다.

- 준비. 레지스터는 x와 y가 화면의 한 점을 지정하고 r이 x축에서 시계 반대 방향으로 라디안 단위로 회전하는 삼중 <x.y.r\>입니다.

INTENSITY라고 불리는 강도는 실수입니다.

- 범위는 0부터 1까지입니다. 0은 검은색이고, 1은 디스플레이가 가능한 최대 밝기이며, 사이의 숫자는 강도 차이의 상대적 로그를 지정합니다.

```text
      Character frame size.

      Blink bit.

   BUFFER BUILDING
```

- 세미트리의 터미널 노드는 세미트리 이름이거나 디스플레이 버퍼입니다. 디스플레이 버퍼는 bufstuff라고 하는 일련의 논리적 엔터티입니다.

버퍼가 초기화되면 비어 있습니다. 그렇지 않은 경우

- 매개변수는 초기에 추가되며, 세미 트리의 마지막 노드 표시가 끝날 때 적용되는 매개변수는 이 노드 표시에 적용됩니다.

- 버퍼가 구축되면 논리적 엔터티가 추가됩니다. 버퍼 이름으로 설정되면 버퍼가 닫히고 추가 추가가 금지됩니다. 트리 작성 명령문에 사용될 수 있도록 설정된 버퍼 이름만 있습니다.

```text
   LOGICAL INPUT DEVICES

      Wand

      Joy Stick

      Keyboard

      Buttons

      Light Pens

      Mice

   AUDIO OUTPUT DEVICES

   .end
```

---
# **SAMPLE PROGRAMS**

디스플레이와 키보드를 tty로 실행하는 프로그램입니다.

NLS를 실행하려면

```text
      input part

      display part

         DEMAND MESSAGE;
```

- 길이가 "O DO"인 동안

- ITHCASE GETBYTE OF Begin

- ITHCASE GETBYTE OF %파일 영역 uipdate% BEGIN

```text
               %literal area%

               %message area%

               %name area%

               %bug%

               %sequence specs%

               %filter specs%

               %format specs%

               %command feedback line%

               %filer area%

               %date time%

               %echo register%

           BEGIN %DEL control%
```

---
# **DISTRIBUTION LIST**

스티브 카

- 컴퓨터공학과 University of Utah Salt Lake City, Utah 84112 전화 801-322-7211 X8224

```text
   Steve Crocker
```

볼터 홀

- University of California Los Angeles, California 전화 213-825-4864

```text
   Jeff Rulifson

      Stanford Research Institute
      333 Ravenswood
      Menlo Park, California  94035
      Phone 415-326-6200 X4116

   Ron Stoughton
```

컴퓨터 연구실

- University of California Santa Barbara, California 93106 전화 805-961-3221

```text
   Mehmet Baray
```

코리 홀

- University of California Berkeley, California 94720 전화 415-843-2621

```text
        
```