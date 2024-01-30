

```text
Network Working Group                                         J. Kreznar
Request for Comments: 17                                             SDC
Category: Informational                                   27 August 1969

                  Some Questions Re: HOST-IMP Protocol
```

1. BBN 1822, 11페이지에 표시된 대로 링크 자동 삭제는 좋지 않은 것 같습니다.

a\) 링크 사용은 시간 공유 터미널\(메시지 사이의 무한한 시간\)을 사용하는 사람의 사용에 따라 달라질 수 있습니다.

b\) 링크를 사용하는 프로그램은 다음과 같은 이유로 인해 속도가 느려질 수 있습니다.

```text
        i)  Busy HOST (many jobs)

        ii) Much local I/O and/or CPU time between messages - is it
            that, if a HOST's user fails to use a link for 15 seconds,
            the HOST network program must generate a dummy message
            merely to keep the link open?
```

2. Steve Crocker, HOST Software, 1969년 4월 7일, 2페이지에서 "IMP와 달리 HOST가 RFNM을 제어할 수 있습니까?"라고 묻습니다. BBN, 보고서 번호 1837, 1969년 7월, 2페이지에 다음과 같이 나와 있습니다. "\(IMP\) 프로그램의 주요 기능은...포함...RFNM 생성..." IMP가 RFNM을 생성한 다음 이를 발견하면 어떻게 될까요? 어떤 이유로 마지막으로 수신된 메시지를 HOST에 적시에 전달할 수 없습니까? 지정된 최대 시간 내에 들어오는 메시지를 수락해야 한다는 HOST에 대한 IMP 제약 조건을 어디에서도 본 기억이 없기 때문에 이는 특히 시급한 것 같습니다.

3. 호스트는 네트워크로 메시지 전송을 반복할 준비가 되어 있어야 합니다\(예: 페이지 17, BBN 1822 참조\). 따라서 특수 폐기 가능한 NOP 메시지\(페이지 12, BBN 1822\)가 필요한 이유입니다.

4. BBN 1822의 23페이지 중간 단락인 "임의의 지연"은 위의 1에서 문제가 된 자동 링크 삭제와 일치하지 않는 것 같습니다. 일반적으로 관련 시간은 여러 자릿수로 다르지만 우선순위가 높은 비네트워크 HOST 책임으로 인해 다음 비트가 오랫동안 지연될 수 있습니다.

```text
    1.  Abhi Bhushan, Proj. MAC         10.  Sal Aranda, SDC
    2.  Steve Crocker, UCLA             11.  Jerry Cole,  "
    3.  Ron Stoughton, UCSB             12.  John Kreznar,"
    4.  Elmer Shapiro, SRI              13.  Dick Linde,  "
    5.  Steve Carr, Utah                14.  Bob Long,    "
    6.  John Haefner, RAND              15.  Reg Martin,  "

    7.  Paul Rovner, LL                 16.  Hal Sackman, "
    8.  Bob Kahn, BB & N                17.  C. Weissman, "
    9.  Larry Roberts, ARPA
```

- \[ 이 RFC는 입력을 위해 기계 판독 가능한 형식으로 작성되었습니다. \] \[ Marc Blanchett의 온라인 RFC 아카이브에 3/00 \]

```text
Network Working Group                                            R. Kahn
Request for Comments: 17a                    Bolt Beranek and Newman Inc
                                                             August 1969

                 Re: Some Questions Re: HOST-IMP Protocol
```

다음 의견은 NWG에서 제기된 JOHN KREZNAR의 질문에 대한 답변입니다:- 17

IMP의 링크 테이블에서 링크 항목을 삭제해도 일반적으로 해당 IMP 사이트의 호스트 전송\(또는 수신\)에는 아무런 영향이 없습니다. 메시지 사이에 링크를 사용하지 않는 것과 메시지를 송수신하는 도중에 호스트 프로그램의 지연으로 인해 링크를 사용하지 않는 것을 구분해보자. 호스트가 링크 테이블에 항목이 없는 링크에서 메시지를 전송하면 해당 항목이 거기에 삽입됩니다. 링크는 사실상 항상 열려 있으므로 링크를 "열린" 상태로 유지하기 위해 "더미" 호스트 메시지가 필요하지 않습니다. 항목이 삭제된 직후 링크 테이블이 가득 차는 경우\(예상하지 않는 상황\)에만 지연이 발생할 수 있습니다.

호스트 프로그램에 의해 발생한 임의의 지연도 링크 항목 삭제 절차와 일치하지 않습니다. 소스 IMP에서 전송하는 동안 링크 테이블에 처음 액세스하면 링크가 차단되고 RFNM이 반환되면 차단이 해제됩니다. 차단되지 않은 전송 링크 항목만 사용하지 않고 30초 후에 삭제됩니다. 임의의 지연을 언급하는 23페이지의 설명은 호스트/IMP 인터페이스가 호스트와 IMP 간에 비트를 비동기적으로 전송하도록 설계된 경우에만 하드웨어에 영향을 주기 위한 것입니다.

RFNM은 메시지가 호스트에 대한 대상 IMP의 출력 큐의 헤드에 도달할 때\(즉, 메시지가 호스트로 전송되기 직전\) 대상 IMP에서 소스 IMP로 반환됩니다. 대상 IMP가 전체 메시지를 호스트에 전달할 수 없는 경우 RFNM의 조기 릴리스로 인해 최대 하나의 메시지가 해당 IMP에 도착할 수 있습니다. 새 메시지는 이후 호스트에 대한 출력 대기열의 끝 부분에 위치하므로 적절한 메시지 도착 순서가 보존됩니다.

NOP 메시지는 호스트와 해당 IMP 간의 통신을 시작하는 동안 사용할 수 있는 특수 제어 메시지입니다. 물론 호스트는 이 기간 동안 NOP 메시지 전송을 거부할 수 있지만 IMP 시작 후 또는 IMP 시작 후 처음으로 수신된 메시지는 다음과 같습니다.

호스트 준비 표시기가 켜져 있으며 IMP에 의해 폐기될 수 있습니다. 우리는 네트워크로의 전송을 반복하기 위해 호스트를 준비할 것을 요구하지 않습니다.

답장. 칸 볼트 BERANEK AND NEWMAN INC.

- \[ 이 RFC는 입력을 위해 기계 판독 가능한 형식으로 작성되었습니다. \] \[ Marc Blanchett의 온라인 RFC 아카이브에 3/00 \]