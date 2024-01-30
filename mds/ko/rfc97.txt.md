

```text
NETWORK WORKING GROUP                                           NIC 5740
Request for Comments #97                                  John T. Melvin
                                                       Richard W. Watson
                                                                 SRI-ARC
                                                        15 February 1971
```

- 제안된 텔넷 프로토콜의 첫 번째 컷

---
# **1    Introduction**

- 이 문서에서는 제안된 Telnet 프로토콜의 첫 번째 부분을 설명합니다. \_Telnet\_은 \_사용자의\_ \_사이트\_에서 실행되고 타자기와 같은 터미널을 활용하여 ARPA 네트워크를 통해 원격 \_서버\_ \_사이트에서 대화형 서비스를 얻을 수 있도록 하는 프로세스입니다. 이 문서는 NIC\(Network Information Center\)에 대한 온라인 액세스를 허용하는 프로토콜에 대한 사양을 설정해야 하는 필요성에 의해 작성되었습니다. 네트워크 정보 센터에서 실행되는 온라인 시스템을 NLS\(NIC\)라고 합니다. NIC에 대한 액세스 사양을 설정하는 문제에 대해 생각하면서 우리는 유사한 특성을 가진 다른 시스템에도 적용할 수 있도록 아이디어를 일반화하려고 노력했습니다. 우리는 여기에 명시된 모든 요구 사항을 준수하기 어려울 수 있는 다른 터미널 하드웨어-소프트웨어 분야가 있다는 것을 알고 있으므로 최종 Telnet 프로토콜은 이 NWG/RFC에 명시된 것과 다를 것입니다. 우리 모두가 도달해야 할 한 가지 결론은 네트워크와의 연결로 인해 모니터 및 터미널 제어 하드웨어에서 터미널과 해당 문자 스트림을 처리하는 보다 표준적인 방법을 사용하게 될 수 있다는 것입니다. 그 동안 우리는 NWG 하위 그룹이 각 사이트의 하드웨어-소프트웨어 요구 사항에 대한 조사와 함께 진행 중인 동일한 주제에 대한 이 문서와 다른 문서를 통해 초기 표준 네트워크 Telnet 프로토콜이 합의될 수 있기를 바랍니다. 대화형 네트워크 사용이 네트워크 프로토콜 발전에 대한 추가 방향을 나타낼 수 있도록 가능한 한 빨리 사용자를 네트워크에 연결하는 것이 중요하기 때문입니다. 다음으로 우리는 몇 가지 설계 문제의 개요를 설명하고 NLS\(NIC\)와 같은 시스템에 대한 액세스 문제를 해결하기 위한 몇 가지 규칙을 제안하고 추가 연구가 필요한 몇 가지 문제를 나타냅니다. NLS\(NIC\) 액세스를 위해 제안된 규칙은 부록 A에 요약되어 있습니다.

---
# **2    Some Design Problems**

```text
   2A.  Basic Assumption
```

- Telnet 프로세스의 기능은 사용자 사이트의 터미널을 네트워크를 통해 서버 사이트에 "직접" 연결된 터미널과 논리적으로 동일하게 표시하는 것입니다. 이 기본 기능에는 여러 가지 의미가 있습니다.

- i\) 서버 시스템 단말이 생성할 수 있는 모든 코드를 사용자가 생성할 수 있어야 한다. 네트워크 정보 센터 및 기타 일부 사이트의 경우 사용자가 네트워크에 대한 입력으로 128개의 ASCII 문자 코드를 모두 생성할 수 있도록 키 입력 규칙을 갖는 것이 합리적인 요구 사항인 것 같습니다. 다른 문자 코드를 사용하는 다른 사이트에서는 해당 코드를 네트워크에 제공하기 위해 Telnet 프로세스가 필요할 수 있습니다.

- ii\) 사용자는 자신의 로컬 시스템으로 다시 탈출하거나 서버 프로세스에서 서버 시스템으로 탈출할 수 있어야 합니다.

- iii\) 한 번에 한 줄 시스템의 텔넷은 한 번에 한 문자 시스템 및 한 번에 한 줄 시스템과 작동할 수 있어야 하며 한 번에 한 줄 시스템의 텔넷은 다음과 같아야 합니다. 한 번에 한 줄 및 한 번에 문자 시스템으로 작업할 수 있습니다.

```text
   2B   Echo Control
```

- Telnet 연결은 실제로 네트워크 전송과 관련하여 전이중이기 때문에 반이중 또는 전이중이라는 용어 대신 에코 제어라는 용어를 사용합니다. 세 가지 최종 사례를 고려해야 합니다.

```text
      Case 1 - Character-at-a-time serving site echoed

      Case 2 - Character-at-a-time user site echoed

      Case 3 - Line-at-a-time user site echoed
```

일부 서비스 제공 사이트는 세 가지 경우 모두에서 작동할 수 있으며 모드를 설정하려면 일부 규칙이 필요합니다. 엄밀히 말하면, 어떤 키를 눌렀을 때 어떤 문자가 에코되는지는 서비스 사이트에서는 중요하지 않습니다. 하지만 사용자에게 나타나는 타이프스크립트의 차이를 최소화하려고 노력하고 싶을 수도 있습니다.

```text
   2C   Format Control Characters
```

- 가로 탭\(HT\), 세로 탭\(VT\), 폼 피드\(FF\), 줄 바꿈\(LF\), 캐리지 리턴\(CR\)의 형식 제어 문자는 사례 2와 3에서 일관된 방식으로 처리되어야 합니다. 위에. 위의 사례 1을 사용하면 상황이 단순화됩니다.

```text
   2D   Network Message Boundaries
```

- NCP 대 NCP 프로토콜은 네트워크 메시지 경계가 사용자 프로세스에 보이지 않도록 지정되었습니다. 이 목표가 유지된다면 좋겠지만, 일부 line-at-a-time 시스템에서는 어려울 수도 있습니다.

2E 구현 협약

- 위의 문제를 해결하기 위한 관례는 서버 사이트의 Telnet 프로세스에서 수신한 문자 스트림이 "direct1y" 연결된 터미널에서 문자 입력이 입력되고 출력되는 서버 모니터의 해당 지점에 입력된다고 가정하면 가장 간단하게 설정됩니다. 서버 프로세스는 정상적인 문자 출력이 입력되는 모니터 지점에 입력됩니다. 서버 NCP는 정상적인 모니터 문자 출력이 획득되는 지점에서 입력을 받습니다. 즉, 서버 프로세스는 NCP 버퍼에서 직접 입력을 얻거나 NCP 버퍼로 출력하는 대신 서버 모니터 문자 버퍼에서 입력을 얻고 출력을 이러한 버퍼로 보냅니다.

- 반면 Telnet 프로세스는 로컬 NCP에서 직접 문자 스트림을 얻고 로컬 NCP로 보냅니다.

- 양쪽 끝의 사용자 프로세스가 NCP와 직접 통신하는 다른 상황이 존재합니다. 따라서 NCP와 사용자 프로세스 간의 통신에는 두 가지 연결 모드\(사용자 프로세스-모니터-NCP 또는 사용자 프로세스-NCP\)를 모두 사용할 수 있는 것이 좋습니다. 이러한 모드는 사용자 프로세스의 프로그램 제어 하에 설정됩니다. 로그인 절차 중 그리고 서버 프로세스에 의해 변경될 때까지 초기 네트워크 규칙은 모니터에서 문자를 얻고 모니터로 문자를 보내는 것입니다. 서버 NCP는 모니터와도 통신합니다. 이 구성표는 그림 1에 나와 있습니다.

- 그러한 유연성의 동기는 아래 논의에서 더 명확해질 수 있습니다.

---
# **3    Proposed Telnet Conventions**

3A 서버 사이트는 명시적으로 다르게 명령될 때까지 사용자 사이트 프로세스에 의해 반향이 수행되는 것으로 처음에 가정합니다. 사용자 사이트가 한 번에 문자를 보낼 수 있는 경우 연결 및 로그인이 설정된 후 사용자는 Lo 서버 사이트 에코를 명령으로 서버 사이트로 전환한 다음 명령\(서버 사이트에는 보이지 않음\)을 전환할 수 있습니다. 로컬 Telnet을 사용하여 에코 모드도 변경할 수 있습니다.

3B 서버 프로세스는 서버 프로세스에 "직접" 연결된 터미널이 생성할 수 있는 동일한 문자 집합을 수신한다고 가정합니다. \(최소 128자 ASCII를 권장합니다.\) 사용자의 Telnet은 대문자 및 소문자 코드와 제어 코드를 모두 생성할 수 있도록 두 문자 시퀀스를 인식해야 할 수도 있습니다. 사용자가 단일 케이스 터미널의 기본 케이스로 대문자 또는 소문자를 설정하고 케이스 이동 문자를 지정할 수 있도록 하는 것이 좋습니다. 사용자는 또한

```text
   character to indicate that the next character struck is to be
   converted to the appropriate control character code.  This latter
   convention enables control codes directly generated at the terminal
   to be recognized by the user's system thus enabling escape to the
   user system.  Creating a convention allowing all control codes to
   enter the network and allowing output of the network to feed into the
   server monitor before entering the server process, gives a simple
   mechanism for generating an escape to     many existing systems.
   (The problem is more complicated than this for some systems and we
   discuss it further below.)
```

3C HT, VT, FF의 로컬 에코의 의미에 대한 네트워크 표준을 설정하거나 이러한 문자의 의미를 서버 프로세스로 전송하기 위한 규칙을 설정하는 것이 좋습니다. 예를 들어 NLS\(NIC\)는 프린트 헤드의 위치를 ​​추적해야 하며 이러한 규칙이 없으면 이러한 문자 코드를 공백과 줄 바꿈으로 변환합니다. 이는 출력 시 페이지 모양이 입력 시 페이지 모양과 다를 수 있음을 의미합니다. 출력 페이지를 입력에 나타난 대로 형식화할 수 있다면 사용자에게 도움이 될 것입니다.

3D LF 문자는 서버 시스템에 "직접" 연결된 터미널에서 줄 바꿈 키를 눌러 생성된 것처럼 처리됩니다.

3E 캐리지 리턴\(CR\) 문자는 상당한 어려움의 원인이 될 수 있습니다. 예를 들어, 입력 시 서로 다른 시스템과 서로 다른 시간의 동일한 시스템이 서로 다른 코드를 터미널과 사용자 프로세스에 에코하고 전송할 수 있습니다. 일부 모니터 시스템에서는 아무것도 에코하지 않고 CR 또는 CRLF만 에코합니다. 일부 시스템은 CR, CRLF 또는 EOL\(End of Line Code\)을 사용자 프로세스에 전송합니다. 사용자 프로세스는 에코를 제어하거나 에코를 추가할 수 있습니다. 네트워크 연결의 각 끝과 서로에 대해 존재할 수 있는 조합을 고려할 때, 2A의 정의와 2E의 구현 규칙을 가정하지 않으면 혼란이 존재할 수 있습니다. 이러한 가정은 CR이 발생하면 CR이 네트워크를 통해 전송된다는 것을 의미합니다. 사용자 모니터 시스템 또는 터미널 제어 하드웨어가 CR을 CRLF 또는 EOL로 변환하는 경우 Telnet 프로그램은 이를 다시 CR로 변환해야 합니다. CR이 서버 모니터에 도달하면 서버 프로세스에 대해 적절하게 처리됩니다.

- 서버 시스템에서 에코를 처리할 때 적절한 코드가 에코됩니다. CRLF를 수신한 사용자 Telnet은 특정 터미널에 대한 캐리지 이동 타이밍을 처리하기 위해 적절한 Null로 CRLF를 채울 수 있습니다.

```text
        When echoing is handled by the user system it would be ideal if
   the user's Telnet or system used the same echo convention as the
```

서버 시스템이겠죠. 이는 Telnet이 연결할 수 있는 다양한 시스템에 대한 에코 규칙 테이블을 가지고 있어야 하거나 서버 시스템이나 프로세스에서 이 정보를 얻을 수 있거나 그 반대의 경우도 가능하다는 것을 의미합니다.

- 초기 Telnet 프로토콜의 경우 이는 필요하지 않을 수 있습니다. 사용자 시스템은 수신된 각 CR에 대해 CRLF를 기본값으로 표시하고 에코할 수 있습니다. 이 기본값은 우리가 익숙한 모든 상황과 NIC에 대해 만족스러울 것입니다.

3F 문자 및 한 번에 한 줄 시스템에서의 통신을 위해 Telnet 프로세스는 EOS\(End of Stream\)라고 하는 문자\(사용자 지정 가능\)를 인식해야 할 수도 있습니다. 이 문자는 다음 설명에서 정의된 기능을 갖습니다. 중요한 점은 네트워크 기능으로서의 스트림 끝과 사용자 또는 서버 시스템 기능으로서의 라인 끝을 구별하는 것입니다. 먼저 한 번에 한 줄씩 시스템을 고려하십시오. 우리는 한 번에 한 줄씩 처리하는 시스템에 대한 경험이 많지 않으므로 다음 내용에 대해서는 추가 연구와 설명이 필요합니다. 우리가 알고 있듯이 한 줄 단위 시스템은 CR이나 중단 신호와 같은 문자를 사용자 프로세스를 깨우고 텍스트 줄을 전송하도록 하는 코드로 인식합니다. NLS\(NIC\)의 관점에서 보면 사용자가 적절한 경우 CR로 끝나는 텍스트 줄을 입력할 수 있고 때로는 CR로 끝나지 않는 텍스트를 입력할 수 있다는 것이 중요합니다. \(NLS\(NIC\)에 대한 명령문은 "임의" 길이의 텍스트 문자열이며 그 안에 CR이 필요하지 않습니다. 출력 시 해당 줄은 사용자의 \(사용자 정의 가능\) 페이지 경계에서 접혀집니다.\)

- 요구되는 것의 예로 사용자 시스템이 CR을 라인 끝으로 인식하는 경우를 생각해 보자. 이 경우 CR이 수신되면 Telnet이 활성화됩니다. 이 경우 CR 코드를 문자 그대로 Telnet 출력 버퍼에 입력하는 것이 좋습니다. CR 앞에 EOS 문자가 오면 CR을 Telnet 출력 버퍼에 배치하면 안 됩니다. 네트워크를 통한 전송은 EOS가 수신될 때 또는 Telnet 출력 버퍼가 채워질 때 자동으로 이루어질 수 있습니다. 한 번에 한 줄 시스템에서 한 번에 한 문자 시스템으로 전송하려면 네트워크를 통해 한 문자를 가져오려면 세 개의 키를 어색하게 눌러야 할 수 있습니다.

```text
        Now consider transmission for a character-at-a-time system to a
   server line-at-a-time system.  A similar problem to the one to be
   described also exists between line-at-a-time systems.  Given the
   definition of an EOS character different from CR, a line can be
   buffered up until the EOS is received and then sent without the EOS.
   How is the serving system to know that a line has been sent?  One way
   would be for the serving NCP to recognize message boundaries.  This
   convention would violate a design goal.  Another way would be for the
```

사용자 Telnet을 사용하여 NCI에 INS 명령을 보내도록 요청합니다. INS 유형의 제어 명령을 보내면 네트워크에 경쟁 조건이 발생할 수 있으므로 Telnet 프로세스와 함께 사용하기 전에 조사해야 합니다. 우리가 알고 있는 일부 라인 단위 시스템에는 라인 끝 신호를 인식하는 특수 하드웨어가 있으므로 소프트웨어 제어 신호를 사용하여 이 하드웨어와 호환될 수 있는 방법이 필요합니다. 이 문제는 추가 NWG 하위 그룹 연구로 남겨 둡니다.

3G 이제 원격 서버 시스템의 중단 또는 탈출 문제로 돌아갑니다. 출력이 진행 중일 때 입력 키보드를 잠그지 않는 시스템에서는 특별한 중단 신호가 탈출 신호가 아닌 한 위에 설명된 메커니즘과 규칙이 적절해 보입니다. 후자의 경우에는 더 많은 연구가 필요합니다. 출력이 발생하는 동안 입력을 허용하지 않는 시스템에서는 이러한 터미널 규칙의 결과를 감수해야 하며 이스케이프 코드가 전송되기 전에 출력이 중지될 때까지 기다려야 할 수 있습니다. 키보드가 잠겨 있고 이탈 중단 신호가 사용자 시스템으로 전송될 수 있는 경우 출력이 터미널로 이동하는 것을 방지할 수 있지만 사용자가 Telnet 프로세스에 전송을 알릴 수 있을 때까지 서버 사이트에서 이를 계속 수신할 준비가 되어 있어야 합니다. 서버 사이트에 대한 인터럽트 또는 탈출 신호. 이는 다시 추가 연구가 필요한 문제입니다.

- 네트워크정보센터의 온라인 시스템은 한 번에 한 문자씩 모니터하는 시스템으로 운영되며, 본 논문에서 정한 규정을 따르면 접근에 적합하다. 이러한 규칙은 부록 A에 요약되어 있습니다.

---
# **APPENDIX A**

SRI-네트워크 정보 센터에 대한 네트워크 연결 프로토콜

```text
   1    Initial Connection Protocol
```

- NIC에 대한 연결 설정은 NWG/RFC 80 NIC\(5608,\)의 섹션 II에 제시된 것과 동일합니다. 여기에 재현되어 있습니다:

```text
   Telnet contacts NIC

   NIC <- user site

        RTS <us> <l> <p>

             NIC logger is socket 1

   user site <- NIC

        STR <l> <us> CLS <l> <us>

             if accepted

        CLS <l> <us>

             if rejected

   assuming NIC accepts

   user site <- NIC

        STR <ss+l> <us>

        RTS <ss> <us+l> <q>

             NIC receives text thru local socket ss from remote
             socket us+l via link q

   assuming user site accepts

        NIC <- user site

             STR <us> <ss+l>

             RTS <us+l> <ss> <r>
```

- NIC는 링크 r을 통해 로컬 소켓 ss+l을 통해 원격 소켓 us에 텍스트를 보냅니다.

```text
                    .
                    .
                    .

        user site <- NIC

             ALL <q> <space>

                    .
                    .
                    .

        NIC <- user site

             ALL <r> <space>

   2    Connection Breaking Protocol
```

- 문서 #1 NIC\(5143,\)에 따라 두 연결 각각에 대해 NCP 간에 CLS 거래가 이루어집니다.

- 일부\(아직 지정되지 않은\) "합리적인" 시간 동안 상호 작용이 없으면 NIC에 의해 시작되는 연결의 CLS 아웃이 발생하도록 NIC 연결에 시간 초과를 설정하기로 결정할 수 있습니다.

```text
   3    Third Level Protocol
```

- 소켓 ss를 통해 NIC가 수신한 처음 8비트는 NWG/RFC #63, NIC\(4963,\)에 따라 8비트 ASCII 스트림이 뒤따르도록 지정하는 메시지 데이터 유형이어야 합니다.

- 즉, 처음 8비트는 00000001입니다.

- 소켓을 통해 Telnet이 수신한 처음 8비트는 메시지 데이터 유형 l을 나타냅니다. 각 네트워크 메시지는 8비트의 정수배를 가져야 합니다. NWG/RFC #63, NIC\(4963,\)의 제안과 다른 네트워크 표준이 확립되면 이 프로토콜을 준수하도록 변경합니다.

- NIC는 NCP 생성 인터럽트를 비활성화합니다. 즉,

- INR은 무시됩니다.

- INS는 원격 호스트로 전송되지 않습니다.

```text
   4    NLS(NIC) Character Conventions of Interest to Telnet
```

- 반향은 NIS\(NIC\)의 제어 하에 있거나 사용자 사이트의 제어 하에 있을 수 있습니다. 아래에서 에코를 언급할 때 NLS\(NIC\)의 제어를 의미합니다. 반향이 사용자 사이트에서 처리될 때 사용자는 자신의 사이트의 반향 규칙을 따르도록 NLS\(NIC\) 출력 규칙을 설정해야 합니다. NLS\(NIC\)는 달리 명시적으로 명령하지 않는 한 사용자 사이트에서 에코를 처리한다고 가정합니다.

```text
      Format affecting control characters

         horizontal tab
```

- 다음\(사용자 정의 가능\)까지의 공백은 에코와 출력 모두에서 중지됩니다.

- 리터럴 입력 중이면 파일을 ASCII '11로 입력합니다.

```text
         form feed
```

- 캐리지 리턴 및 \(사용자 정의 가능\) 에코 및 출력에 대한 적절한 줄 바꿈 수.

```text
                 If during literal input, enters file as ASCII '14

         vertical tab

                 carriage return and (user definable) appropriate number
            of line feeds on echo and output

                 if during literal input, enters file as ASCII '13

         carriage return

                 carriage return followed by line feed on echo and
            output

                 if during literal input, enters file as EOL (see below)

         line feed

                 line feed on echo and output

                 enters file as ASCII '12 on literal input

         EOL (end of line)

                 presently ASCII code '37

                 carriage return followed by line feed on echo and
            output

                 if during literal input, enters file as ASCII '37
```

- 사용자 시스템이 Telnet으로 보내기 전에 자동으로 LF를 CR에 추가하거나 CR을 ASCII '37이 아닌 일부 EOL 코드로 변환하는 경우 Telnet은 NLS\(NIC\)에 CR 또는 ASCII '37만 보낼 것으로 예상합니다. CRLF를 받으면 출력 시 CRLFLF를 보냅니다.

```text
   5 NLS(NIC) Interrupt Attention Convention
```

- 텍스트 입력 스트림의 \(사용자 정의 가능\) ASCII 코드는 실행 프로세스를 중단하고 기본 NLS\(NIC\) 명령 프로세서로 제어권을 반환하는 데 사용됩니다.

- 이 코드는 현재 DEL\(ASCII '177\)입니다.

- NIC 모니터로 탈출: NIC 사용에 필요한 모든 작업은 NLS\(NIC\) 내에서 수행할 수 있으므로 탈출이 필요하지 않습니다.

- 문자 집합: Telnet 프로세스에서 일부 키 지정 규칙 집합에 따라 모든 128 ASCII 코드를 생성할 수 있도록 강력히 권장합니다. NLS\(NIC\)를 사용하면 대문자와 소문자 그래픽이 있는 장치에서 가장 편안하게 느낄 수 있지만 단일 케이스 장치에도 서비스를 제공할 수 있습니다. 전체 ASCII 세트를 전송할 수 없는 경우 유용한 서비스를 제공할 수 있지만 처리해야 하는 특수한 경우를 최소화하고 싶습니다. 전체 ASCII 세트를 제공할 수 없는 사이트는 당사에 문의하시기 바랍니다.

```text
         +----+                      |
         |    |        Server        |
         |    |        Program       |
         |    |                      |
         +----+                      |
          ^ |                        |
          | v                        |
         +----+        Terminal      |
         |    |        control       |
         |    |        software      |    SERVER
         |    |        and           |     SITE
         +----+        possibly      |
          ^ |          hardware      |
          | v                        |

         +----+                      |
         |    |                      |
         |    |        NCP           |
         |    |                      |
         +----+                      |
          ^ |                        |
          | v                        |

          . .
          . .                                            Figure 1 -
          . .
          . .                                        Telnet Connection

          ^ |
          | v
         +----+                      |
         |    |                      |
         |    |        NCP           |
         |    |                      |
         +----+                      |
          ^ |                        |
          | v                        |
         +----+                      |
         |    |                      |
         |    |        Telnet        |
         |    |                      |
         +----+                      |
          ^ |                        |    USER
          | v                        |    SITE
         +----+        Terminal      |
         |    |        control       |
         |    |        hardware-     |
         |    |        software      |
         +----+                      |
          ^ |                        |
          | v                        |
         +----+                      |
         |    |        User          |
          \   |        terminal      |
           \--+                      |
```

- \[ 이 RFC는 입력을 위해 기계 판독 가능한 형식으로 작성되었습니다. \] \[ Tony Hansen의 온라인 RFC 아카이브에 08/08 \]