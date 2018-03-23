import java.net.MalformedURLException;
import java.rmi.Naming;
import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.util.Scanner;

public class OperationClient {
    public static void main(String[] args) throws RemoteException, NotBoundException, MalformedURLException {
		String host = "";

		try{
			host = args[0];
		} catch (ArrayIndexOutOfBoundsException e){
			throw new IllegalArgumentException("You must provide the host as argument. Ex: java OperationClient localhost");	
		}

        Scanner scanner = new Scanner(System.in);
        System.out.println("Insert an mathematical operation. Ex: 1 + 2:");
        int a = scanner.nextInt();

        String string = scanner.next();
        int b = scanner.nextInt();
        scanner.close();

        Operation operation = OperationClient.connect(host);
        operation.set_operands(a, b);

        int result = OperationClient.calculate(a, b, string, operation);
        System.out.println("Result: " + result);
    }

    private static Operation connect(String host) throws RemoteException, NotBoundException, MalformedURLException {
        Operation operation = (Operation) Naming.lookup("rmi://" + host + "/Operation");

        return operation;
    }

    private static int calculate(int a, int b, String string, Operation operation) throws IllegalArgumentException, RemoteException {
        int result = -1;
        switch (string) {
            case "+": {
                result = operation.sum();
                break;
            }
            case "-": {
                result = operation.sub();
                break;
            }
            case "*": {
                result = operation.mult();
                break;
            }
            case "/": {
                result = operation.div();
                break;
            }
            default: {
                throw new IllegalArgumentException("Can't calculate. Invalid operator");
            }
        }
        return result;
    }
}
