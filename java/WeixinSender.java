package com.jysong.jenkins.newplugin;
 
import org.python.core.PyFunction;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;


public class WeixinSender extends Sender {
	
	private  PythonInterpreter interpreter;
	private  PyFunction func;
	
	public void initial() {	
		
	}
 
	public boolean GroupSend(String type, String msg, String ext) {
		interpreter = new PythonInterpreter(); 
		interpreter.execfile("E:\\opensource\\CI-weixin\\weixin\\wxsender.py");
		func = (PyFunction)interpreter.get("sendGroup",PyFunction.class);      
	    func.__call__(new PyString(msg));       
	    return true;
	}
 
	public boolean SendByID(String type, String ID, String msg, String ext) {
		 interpreter = new PythonInterpreter(); 
		 interpreter.execfile("E:\\opensource\\CI-weixin\\weixin\\wxsender.py"); 
	     func = (PyFunction)interpreter.get("sendByFakeid",PyFunction.class);      
	     func.__call__(new PyString(ID), new PyString(msg));   
	     return true;
	}

}
