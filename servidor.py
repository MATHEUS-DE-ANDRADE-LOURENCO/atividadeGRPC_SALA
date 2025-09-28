# server.py
from concurrent import futures
import grpc
import urls_pb2
import urls_pb2_grpc
import hashlib
import time
import threading

class EncurtadorServicer(urls_pb2_grpc.EncurtadorURLServicer):
    def __init__(self):
        self.lock = threading.Lock()
        self.db = {}  # codigo -> url_longa

    def _gera_codigo(self, url):
        mash = hashlib.sha256((url + str(time.time())).encode()).hexdigest()
        return mash[:7]

    def EncurtarURL(self, request, context):
            peer = context.peer()
            print(f"[Nova requisição] EncurtarURL chamada por: {peer}")
            url = request.url_longa.strip()
            if not url:
                return urls_pb2.RespostaEncurtar(sucesso=False, msg="URL vazia")

            codigo = self._gera_codigo(url)
            with self.lock:
                self.db[codigo] = url

            url_curta = f"http://localhost:50051/{codigo}"
            print(f"[Requisição] URL encurtada: {url} -> {url_curta}")
            return urls_pb2.RespostaEncurtar(url_curta=url_curta, codigo=codigo, sucesso=True, msg="OK")

    def ObterURLLonga(self, request, context):
            peer = context.peer()
            print(f"[Nova requisição] ObterURLLonga chamada por: {peer}")
            codigo = request.codigo.strip()
            with self.lock:
                url = self.db.get(codigo, "")
            if url:
                print(f"[Requisição] Código encontrado: {codigo} -> {url}")
                return urls_pb2.RespostaObter(url_longa=url, sucesso=True, msg="OK")
            else:
                print(f"[Requisição] Código não encontrado: {codigo}")
                return urls_pb2.RespostaObter(sucesso=False, msg="Código não encontrado")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    urls_pb2_grpc.add_EncurtadorURLServicer_to_server(EncurtadorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor Python gRPC rodando em :50051")
    print("Aguardando novas conexões...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
