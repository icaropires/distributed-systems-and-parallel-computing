package matrixClient;


import matrixClient.wsdl.Operation;
import matrixClient.wsdl.PairInResponse;
import matrixClient.wsdl.PairOutResponse;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.ws.soap.client.SoapFaultClientException;

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

            String[] inputMatrixASize = getMatrixASize(input);
            String[] inputMatrixBSize = getMatrixBSize(input);

            readInputOfMatrices(pairClient, inputMatrixASize, inputMatrixBSize, input);

            generateTasks(pairClient, inputMatrixASize, inputMatrixBSize);


            ArrayList<ArrayList<BigInteger>> result = getCalculatedResult(pairClient, 
                                                                            inputMatrixASize, 
                                                                            inputMatrixBSize);


            for (int i = 0; i < result.size(); i++) {
                for (int j = 0; j < result.get(i).size(); j++) {
                    System.out.print(result.get(i).get(j) + " ");
                }
                System.out.println();
            }

        };
    }

    private ArrayList<ArrayList<BigInteger>> getCalculatedResult(PairClient pairClient, String[] inputMatrixASize, String[] inputMatrixBSize) {
        Integer matrixANumberOfLines = Integer.parseInt(inputMatrixASize[0]);
        Integer matrixBNumberOfColumns = Integer.parseInt(inputMatrixBSize[1]);
        ArrayList<ArrayList<BigInteger>> resultMatrix = new ArrayList<>();
        while(true) {
            for (int i = 1; i <= matrixANumberOfLines; i++) {
                ArrayList<BigInteger> line = new ArrayList<>();
                for (int j = 1; j <= matrixBNumberOfColumns ; j++) {
                    PairOutResponse response = null;
                    try {
                        response = pairClient.pairOut("Element"+i+j);
                    }
                    catch (SoapFaultClientException ex) {
                        continue;
                    }
                    Operation operation = response.getValue();
                    line.add(j-1, operation.getCalculated());
                }
                resultMatrix.add(i-1, line);
                if(resultMatrix.size() == matrixANumberOfLines)
                    return resultMatrix;
            }
        }
    }

    private String[] getMatrixBSize(Scanner input) {
        System.out.println("-------------------");
        System.out.println("Digite o tamanho da matriz B (Linhas Colunas): ");
        return input.nextLine().split(" ");
    }

    private String[] getMatrixASize(Scanner input) {
        System.out.println();
        System.out.println();
        System.out.println("-------------------");
        System.out.println("Digite o tamanho da matriz A (Linhas Colunas): ");
        return input.nextLine().split(" ");
    }

    private void generateTasks(PairClient pairClient, String[] inputMatrixASize,  String[] inputMatrixBSize) {
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
            System.out.println("Digite as " + matrixANumberOfLines + " linhas da matriz A");

            for (int i = 0; i < matrixANumberOfLines; i++) {
                Operation operation = new Operation();
                for (int j = 0; j < matrixANumberOfColumns; j++) {
                    operation.getLine().add(BigInteger.valueOf(input.nextInt()));
                }
                pairClient.pairIn("A" + (i+1), operation);
            }

            System.out.println("Digite as " + matrixBNumberOfColumns + " colunas da matriz B");

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

