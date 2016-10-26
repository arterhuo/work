import org.apache.commons.codec.binary.Base64;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.security.Key;

/**
 * Created by IFT8 on 2016/10/24.
 */
public class AES {
    //密钥算法
    private static final String KEY_ALGORITHM = "AES";

    //加解密算法/工作模式/填充方式,Java6.0支持PKCS5Padding填充方式,BouncyCastle支持PKCS7Padding填充方式
    private static final String CIPHER_ALGORITHM = "AES/ECB/PKCS5Padding";

    private static String initkey() throws Exception{
        KeyGenerator kg = KeyGenerator.getInstance(KEY_ALGORITHM); //实例化密钥生成器
        kg.init(128);                                              //初始化密钥生成器:AES要求密钥长度为128,192,256位
        SecretKey secretKey = kg.generateKey();                    //生成密钥
        return Base64.encodeBase64String(secretKey.getEncoded());  //获取二进制密钥编码形式
    }

    /**
     * 转换密钥
     */
    private static Key toKey(byte[] key) throws Exception{
        return new SecretKeySpec(key, KEY_ALGORITHM);
    }

    /**
     * 加密数据
     * */
    private static String encrypt(String data, Key key) throws Exception{
        Cipher cipher = Cipher.getInstance(CIPHER_ALGORITHM);              //实例化Cipher对象，它用于完成实际的加密操作
        cipher.init(Cipher.ENCRYPT_MODE, key);                               //初始化Cipher对象，设置为加密模式
        return Base64.encodeBase64String(cipher.doFinal(data.getBytes())); //执行加密操作。加密后的结果通常都会用Base64编码进行传输
    }


    /**
     * 解密数据
     * */
    private static String decrypt(String data, Key key) throws Exception{
        Cipher cipher = Cipher.getInstance(CIPHER_ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, key);                          //初始化Cipher对象，设置为解密模式
        return new String(cipher.doFinal(Base64.decodeBase64(data))); //执行解密操作
    }

    public static String encrypt(String data) throws Exception {
        return encrypt(data,key());
    }

    public static String decrypt(String data) throws Exception {
        return decrypt(data,key());
    }

    private static Key key() throws Exception {
        return toKey(Base64.decodeBase64("i/iVsnCsaR+z01nmk7Db4w=="));
    }


    public static void main(String[] args) throws Exception {
        System.out.println(decrypt("9oEHCakGYBGSb2deKSn0lg=="));
    }
}
