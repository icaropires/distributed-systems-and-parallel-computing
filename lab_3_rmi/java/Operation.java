import java.rmi.Remote;
import java.rmi.RemoteException;

public interface Operation extends Remote {
    public void set_operands(int a, int b) throws RemoteException;

    public int sum() throws RemoteException;

    public int sub() throws RemoteException;

    public int div() throws RemoteException;

    public int mult() throws RemoteException;
}
