// cliente.cpp
#include <iostream>
#include <memory>
#include <string>

#include <grpcpp/grpcpp.h>
#include "urls.grpc.pb.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using encurtador::EncurtadorURL;
using encurtador::RequisicaoEncurtar;
using encurtador::RespostaEncurtar;
using encurtador::RequisicaoObter;
using encurtador::RespostaObter;

class EncurtadorClient {
public:
    EncurtadorClient(std::shared_ptr<Channel> channel)
        : stub_(EncurtadorURL::NewStub(channel)) {}

    std::string EncurtarURL(const std::string& url) {
        RequisicaoEncurtar req;
        req.set_url_longa(url);
        RespostaEncurtar res;
        ClientContext ctx;

        Status status = stub_->EncurtarURL(&ctx, req, &res);
        if (status.ok() && res.sucesso()) {
            std::cout << "URL curta: " << res.url_curta() << "\nCodigo: " << res.codigo() << std::endl;
            return res.codigo();
        } else {
            std::cerr << "Erro EncurtarURL: " << status.error_message() << " / " << res.msg() << std::endl;
            return "";
        }
    }

    void ObterURLLonga(const std::string& codigo) {
        RequisicaoObter req;
        req.set_codigo(codigo);
        RespostaObter res;
        ClientContext ctx;

        Status status = stub_->ObterURLLonga(&ctx, req, &res);
        if (status.ok() && res.sucesso()) {
            std::cout << "URL longa recuperada: " << res.url_longa() << std::endl;
        } else {
            std::cerr << "Erro ObterURLLonga: " << status.error_message() << " / " << res.msg() << std::endl;
        }
    }

private:
    std::unique_ptr<EncurtadorURL::Stub> stub_;
};

int main(int argc, char** argv) {
    EncurtadorClient client(grpc::CreateChannel("localhost:50051", grpc::InsecureChannelCredentials()));
    std::string url = "https://example.com/alguma/pagina/muito/comprida";
    std::string codigo = client.EncurtarURL(url);
    if (!codigo.empty()) {
        client.ObterURLLonga(codigo);
    }
    return 0;
}
