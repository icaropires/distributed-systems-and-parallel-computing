import java.net.MalformedURLException;
import java.rmi.Naming;
import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.util.Scanner;

public class OperationClient {
    public static void main(String[] args) throws RemoteException, NotBoundException, MalformedURLException {
		String host = "";

		String current_directory = System.getProperty("user.dir");
		System.setProperty("java.security.policy", "file:///" + current_directory + "/client.policy");

		if (System.getSecurityManager() == null) {
			System.setSecurityManager(new SecurityManager());
		}

		try{
			host = args[0];
		} catch (ArrayIndexOutOfBoundsException e){
			throw new IllegalArgumentException("You must provide the host as argument. Ex: java OperationClient localhost");	
		}

		Operation operation = OperationClient.connect(host);

        Scanner scanner = new Scanner(System.in);
        System.out.println("Insert an mathematical operation. Ex: 1 + 2:");
        int a = scanner.nextInt();

        String operator = scanner.next();
        int b = scanner.nextInt();
        scanner.close();

        operation.set_operands(a, b);

        int result = OperationClient.compute(operation, operator);
        System.out.println("Result: " + result);
    }

    private static Operation connect(String host) throws RemoteException, NotBoundException, MalformedURLException {
		Operation operation = (Operation) Naming.lookup("rmi://" + host + "/Operation");

        return operation;
    }

    private static int compute(Operation operation, String operator) throws IllegalArgumentException, RemoteException {
        int result = -1;
        switch (operator) {
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
                throw new IllegalArgumentException("Can't compute. Invalid operator");
            }
        }
        return result;
    }
}
