package com.jysong.jenkins.newplugin;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

 
import org.apache.commons.httpclient.Header;
import org.apache.commons.httpclient.HttpClient;
import org.apache.commons.httpclient.HttpException;
import org.apache.commons.httpclient.NameValuePair;
import org.apache.commons.httpclient.methods.PostMethod;


public class FeixinSender extends Sender {
	
	private static String PHONE = "13918533241";
    private static String PWD = "244168abc";
    
	public void initial() {
		 
	}
	
	public boolean GroupSend(String type, String msg, String ext) {
		HttpClient client = new HttpClient();
		         
		try {
			FileReader fr = new FileReader("D:\\info.txt");
			BufferedReader br = new BufferedReader(fr);
			String Line;	
			//ʹ��Post����
		    PostMethod post = new PostMethod("http://w.ibtf.net/f.php");
				 
			//��ͷ�ļ�������ת��
			post.addRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=utf-8");
			while ((Line = br.readLine()) != null) {
				String[] result = Line.split(",");
				System.out.println(result[1]);
				NameValuePair[] data ={ 
			                new NameValuePair("phone", PHONE),
			                new NameValuePair("pwd", PWD),
			                new NameValuePair("to",result[1]),
			                new NameValuePair("msg",msg),
			                new NameValuePair("type","0")
			                };
				post.setRequestBody(data);		    		         
				client.executeMethod(post);	              
			    int statusCode = post.getStatusCode();		        
			     if(statusCode != 200){
			        	br.close();
						fr.close();
						//�ͷ�����
					     post.releaseConnection();
			        	return false;
			        }			        
			   }	
			 //�ͷ�����
		    post.releaseConnection();
			br.close();
			fr.close();
			 	
		} catch ( Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return true;		 
	}
	 
	public boolean SendByID(String type, String ID, String msg, String ext) {
		
		HttpClient client = new HttpClient();
		 
		//ʹ��Post����
		PostMethod post = new PostMethod("http://w.ibtf.net/f.php");
		 
		//��ͷ�ļ�������ת��
		post.addRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=utf-8");
	        
		NameValuePair[] data ={ 
	                new NameValuePair("phone", PHONE),
	                new NameValuePair("pwd", PWD),
	                new NameValuePair("to",ID),
	                new NameValuePair("msg",msg),
	                new NameValuePair("type","0")
	                };
	        
	    post.setRequestBody(data);
	    
	        try {
				client.executeMethod(post);
			} catch (HttpException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	              
	        int statusCode = post.getStatusCode();
	        Header[] headers = post.getResponseHeaders();
	        System.out.println("statusCode:"+statusCode);
	        for(Header h : headers){
	            System.out.println(h.toString());
	            System.out.println("");
	        }
	        
	       //�ͷ�����
	        post.releaseConnection();
	        
	        if(statusCode == 200)
	        {
	        	return true;
	        }
	        else{
	        	return false;
	        }
	}

}
