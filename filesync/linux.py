# import daemon
#
# def run():
#     with open('daemon.log', 'w') as f:
#         while True:
#             # 데몬 프로세스가 실행할 작업 수행
#             f.write("데몬 프로세스 동작 중...\n")
#
# with daemon.DaemonContext(stdout=open('daemon.log', 'w+')):
#     run()
