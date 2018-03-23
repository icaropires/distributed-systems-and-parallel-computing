import java.net.MalformedURLException;
import java.rmi.AlreadyBoundException;
import java.rmi.Naming;
import java.rmi.Remote;
import java.rmi.RemoteException;

public class OperationServer {
    public static void main(String[] args) throws RemoteException, AlreadyBoundException, MalformedURLException {
        Operation operation = new example_Operation();

        Naming.bind("Operation", operation);
        System.out.println("Operation ready!");
    }
}
