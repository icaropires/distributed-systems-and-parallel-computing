package matrixClient;


import matrixClient.wsdl.Operation;
import matrixClient.wsdl.PairInResponse;
import matrixClient.wsdl.PairOutResponse;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.ws.soap.client.SoapFaultClientException;

import java.lang.reflect.Array;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Scanner;

@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @Bean
    CommandLineRunner lookup(PairClient pairClient) {
        return args -> {
            Scanner input = new Scanner(System.in);
            String[] inputMatrixASize = input.nextLine().split(" ");
            String[] inputMatrixBSize = input.nextLine().split(" ");


            readInputOfMatrices(pairClient, inputMatrixASize, inputMatrixBSize, input);

            Integer matrixANumberOfLines = Integer.parseInt(inputMatrixASize[0]);
            Integer matrixBNumberOfColumns = Integer.parseInt(inputMatrixBSize[1]);

            for (int i = 1; i <= matrixANumberOfLines; i++) {
                for (int j = 1; j <= matrixBNumberOfColumns ; j++) {
                    Operation operation = new Operation();
                    operation.getCoordinates().add(BigInteger.valueOf(i));
                    operation.getCoordinates().add(BigInteger.valueOf(j));
                    pairClient.pairIn("nexttask", operation);
                }
            }


            while(true) {
                for (int i = 1; i <= matrixANumberOfLines; i++) {
                    for (int j = 1; j <= matrixBNumberOfColumns ; j++) {
                        PairOutResponse response = null;
                        try {
                            response = pairClient.pairOut("Element"+i+j);
                        }
                        catch (SoapFaultClientException ex) {
                            continue;
                        }
                        Operation operation = response.getValue();
                        System.out.println(operation.getCalculated());
                    }
                }
            }

        };
    }

    private void readInputOfMatrices(PairClient pairClient,
                                     String[] inputMatrixASize,
                                     String[] inputMatrixBSize,
                                     Scanner input) {
        Integer matrixANumberOfLines = Integer.parseInt(inputMatrixASize[0]);
        Integer matrixANumberOfColumns = Integer.parseInt(inputMatrixASize[1]);

        Integer matrixBNumberOfLines = Integer.parseInt(inputMatrixBSize[0]);
        Integer matrixBNumberOfColumns = Integer.parseInt(inputMatrixBSize[1]);

        if(!matrixANumberOfColumns.equals(matrixBNumberOfLines)) {
            System.out.println("NÃO PODE SER MULTIPLICADO");
        }
        else {
            System.out.println("DIGITE AS " + matrixANumberOfLines + " LINHAS DA MATRIX A");

            for (int i = 0; i < matrixANumberOfLines; i++) {
                Operation operation = new Operation();
                for (int j = 0; j < matrixANumberOfColumns; j++) {
                    operation.getLine().add(BigInteger.valueOf(input.nextInt()));
                }
                pairClient.pairIn("A" + (i+1), operation);
            }

            System.out.println("DIGITE AS " + matrixBNumberOfColumns + " COLUNAS DA MATRIX B");

            for (int i = 0; i < matrixBNumberOfColumns; i++) {
                Operation operation = new Operation();
                for (int j = 0; j < matrixBNumberOfLines; j++) {
                    operation.getColumn().add(BigInteger.valueOf(input.nextInt()));
                }
                pairClient.pairIn("B" + (i+1), operation);
            }
        }
    }

}

