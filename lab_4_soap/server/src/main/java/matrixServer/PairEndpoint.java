package matrixServer;

import io.spring.guides.gs_producing_web_service.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;

@Endpoint
public class PairEndpoint {
    private static final String NAMESPACE_URI = "http://spring.io/guides/gs-producing-web-service";

    private PairRepository pairRepository;

    @Autowired
    public PairEndpoint(PairRepository pairRepository) {
        this.pairRepository = pairRepository;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "pairInRequest")
    @ResponsePayload
    public PairInResponse pairIn(@RequestPayload PairInRequest request) {
        System.out.println("***********************************");
        System.out.print("*********" + request.getKey());
        System.out.print(" *********" + request.getValue().getLine());
        System.out.print("*********" + request.getValue().getColumn());
        System.out.print(" *********" + request.getValue().getCoordinates());
        System.out.print("*********" + request.getValue().getCalculated());
        System.out.println("***********************************");

        String key = pairRepository.insertPair(request.getKey(), request.getValue());
        PairInResponse response = new PairInResponse();
        response.setKey(key);

        return response;
    }


    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "pairOutRequest")
    @ResponsePayload
    public PairOutResponse pairOut(@RequestPayload PairOutRequest request) {
        Operation operation = pairRepository.removePair(request.getKey());

        PairOutResponse response = new PairOutResponse();
        response.setValue(operation);
        return response;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "readPairRequest")
    @ResponsePayload
    public ReadPairResponse readPair(@RequestPayload ReadPairRequest request) {
        Operation operation = pairRepository.getPair(request.getKey());
        ReadPairResponse response = new ReadPairResponse();
        response.setValue(operation);
        return response;
    }

}