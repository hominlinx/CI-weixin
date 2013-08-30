package com.jysong.jenkins.newplugin;

public interface SenderIF {
		
		 // ��ʼ��
	     void initial();
	
		 // Ⱥ��
         boolean GroupSend(String type, String msg, String ext);
         
         //���ָ��name����
         boolean SendByID(String type, String ID, String msg, String ext);
}
