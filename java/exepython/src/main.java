

import org.python.util.PythonInterpreter;  
  
import java.io.*;  
import static java.lang.System.*; 
import org.python.core.*;

public class main {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		PythonInterpreter interp = new PythonInterpreter();
		
		/*
		interp.execfile("E:\\opensource\\CI-weixin\\python\\PyWapFetion\\feixintest.py");
		PyFunction func = (PyFunction)interp.get("sendmsg",PyFunction.class);
		
		String mobile = "15721235404";
		String msg = "test";
		func.__call__(new PyString(mobile),new PyString(msg));
		*/
		interp.execfile("E:\\opensource\\CI-weixin\\weixin\\wxsender.py");
		PyFunction func = (PyFunction)interp.get("sendByFakeid",PyFunction.class);
		String fakeid = "2201337020";
		String msg = "test";
		func.__call__(new PyString(fakeid), new PyString(msg));
	}

}
