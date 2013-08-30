package com.jysong.jenkins.newplugin;

public class Sender implements SenderIF {
	
	private Sender weixinSender;
	private Sender feixinSender;
	
	
	public void initial() {
		 
		weixinSender = new WeixinSender();
		feixinSender = new FeixinSender();
		
		weixinSender.initial();
		feixinSender.initial();
	}

	
	public boolean GroupSend(String type, String msg, String ext) {
		 
		 if(type == "weixin"){
			 return weixinSender.GroupSend(type, msg, ext);
		 }
		 else if(type == "feixin"){
			 return feixinSender.GroupSend(type, msg, ext);
		 }
		 else{
			 return false;
		 }	
	}

	
	public boolean SendByID(String type, String ID, String msg, String ext) {
		 
		 if(type == "weixin"){
			 return weixinSender.SendByID(type, ID, msg, ext);
		 }
		 else if(type == "feixin"){
			 return feixinSender.SendByID(type, ID, msg, ext);
		 }
		 else{
			 return false;
		 }
	}
}
