

```text
Network Working Group                                           G. Gregg
Request for Comments: 23                                            UCSB
                                                         16 October 1969

                TRANSMISSION OF MULTIPLE CONTROL MESSAGES
```

사이트의 네트워크 프로그램은 더 많은 정보를 보내거나 받을 수 있도록 준비되어 있어야 합니다.
단일 제어 통신에서 하나 이상의 제어 메시지.

RFNM을 기다리면서 제어 링크가 차단되는 동안에는
특정 원격 호스트에 대한 다수의 제어 메시지가
축적됩니다. 링크가 차단 해제되면 모두 전송되어야 합니다.
단일 커뮤니케이션으로 효율성을 극대화합니다.

수신하려면 다음으로 돌아가는 루프가 필요합니다.
제어가 완료될 때까지 연속적인 제어 메시지를 디코딩하고 조치를 취합니다.
의사소통이 소진되었습니다.