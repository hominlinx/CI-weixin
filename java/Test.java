import org.python.core.PyFunction;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;


public class Test {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		 SenderIF s = new Sender();
		 s.initial();
		 boolean b = s.GroupSend("weixin", "帅哥，现在是群发，收到请回复！", "扩展信息");
		
	}
}
