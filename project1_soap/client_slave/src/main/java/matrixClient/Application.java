package matrixClient;


import matrixClient.wsdl.*;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.ws.soap.client.SoapFaultClientException;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;

@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @Bean
    CommandLineRunner lookup(PairClient pairClient) {
        return args -> {
            while(true) {

                List<BigInteger> coords = getCoordinates(pairClient);

                BigInteger i = coords.get(0);
                BigInteger j = coords.get(1);

                BigInteger result = multiplyLineAndColumn(pairClient, i , j);

                sendResult(pairClient, i, j, result);
            }
        };
    }

    private void sendResult(PairClient pairClient, BigInteger i, BigInteger j, BigInteger result) {
        Operation pairInOperation = new Operation();
        pairInOperation.setCalculated(result);
        PairInResponse pairInResponse = pairClient.pairIn("Element" + i.toString() + j.toString(), pairInOperation);
    }

    private List<BigInteger> getCoordinates(PairClient pairClient) {
        PairOutResponse response = null;
        while (true) {
            try {
                response = pairClient.pairOut("nexttask");
            }
            catch (SoapFaultClientException ex) {
                continue;
            }
            Operation operation = response.getValue();
            return operation.getCoordinates();
        }
    }

    private BigInteger multiplyLineAndColumn(PairClient pairClient, BigInteger i, BigInteger j) {
        ReadPairResponse readPairIResponse = pairClient.readPair("A" + i.toString());
        ReadPairResponse readPairJResponse = pairClient.readPair("B" + j.toString());

        List<BigInteger> line = readPairIResponse.getValue().getLine();
        List<BigInteger> column = readPairJResponse.getValue().getColumn();

        return matrixMultiplication(line, column);
    }

    private BigInteger matrixMultiplication(List<BigInteger> line, List<BigInteger> column) {
        BigInteger sum = BigInteger.valueOf(0);
        for (int i = 0; i < line.size(); i++) {
            BigInteger lineValue = line.get(i);
            BigInteger columValue = column.get(i);

            BigInteger temp = lineValue.multiply(columValue);

            sum = sum.add(temp);
        }

        return sum;
    }


}

