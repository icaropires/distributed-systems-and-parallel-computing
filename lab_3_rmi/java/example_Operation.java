import java.rmi.Remote;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class example_Operation extends UnicastRemoteObject implements Operation {
	private int a;
	private int b;

	public void set_operands(int a, int b){
		this.a = a;	
		this.b = b;
	}

	public int sum() throws RemoteException {
		return this.a + this.b;
	}

	public int sub() throws RemoteException {
		return this.a - this.b;
	}

	public int div() throws RemoteException {
		int result = -1;

		if(b != 0){
			result = this.a / this.b;
		} else {
			System.err.println("Can't divide by zero!");
		}

		return result;
	}

	public int mult() throws RemoteException {
		return this.a * this.b;
	}

	public example_Operation() throws RemoteException {
		super();
		System.out.println("Building object example operation...");
	}
}
