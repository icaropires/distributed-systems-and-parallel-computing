package matrixClient;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.boot.SpringApplication;
import org.springframework.ws.client.core.support.WebServiceGatewaySupport;
import org.springframework.ws.soap.client.SoapFaultClientException;
import org.springframework.ws.soap.client.core.SoapActionCallback;

import matrixClient.wsdl.*;

public class PairClient extends WebServiceGatewaySupport {

    private static final Logger log = LoggerFactory.getLogger(PairClient.class);

    public PairInResponse pairIn(String key, Operation operation) {

        PairInRequest request = new PairInRequest();
        request.setKey(key);
        request.setValue(operation);

//        PairInResponse response = (PairInResponse) getWebServiceTemplate()
//                .marshalSendAndReceive("http://www.webservicex.com/stockquote.asmx",
//                        request,
//                        new SoapActionCallback("http://www.webserviceX.NET/GetQuote"));
        PairInResponse response = (PairInResponse) getWebServiceTemplate().marshalSendAndReceive(request);

        return response;
    }

    public PairOutResponse pairOut(String key) {
        PairOutResponse response = null;
        PairOutRequest request = new PairOutRequest();
        request.setKey(key);

//        PairInResponse response = (PairInResponse) getWebServiceTemplate()
//                .marshalSendAndReceive("http://www.webservicex.com/stockquote.asmx",
//                        request,
//                        new SoapActionCallback("http://www.webserviceX.NET/GetQuote"));
        response = (PairOutResponse) getWebServiceTemplate().marshalSendAndReceive(request);

        return response;
    }

    public ReadPairResponse readPair(String key) {

        ReadPairRequest request = new ReadPairRequest();
        request.setKey(key);

//        PairInResponse response = (PairInResponse) getWebServiceTemplate()
//                .marshalSendAndReceive("http://www.webservicex.com/stockquote.asmx",
//                        request,
//                        new SoapActionCallback("http://www.webserviceX.NET/GetQuote"));
        ReadPairResponse response = (ReadPairResponse) getWebServiceTemplate().marshalSendAndReceive(request);

        return response;
    }
}