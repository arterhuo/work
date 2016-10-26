import com.beust.jcommander.internal.Lists;
import org.apache.commons.codec.binary.Base32;
import org.apache.commons.codec.binary.Hex;
import org.apache.commons.io.FileUtils;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.attribute.DosFileAttributeView;
import java.util.List;


public class GAuth {

    private static String getTOTPCode(String secretKey) {
        String normalizedBase32Key = secretKey.replace(" ", "").toUpperCase();
        Base32 base32 = new Base32();
        byte[] bytes = base32.decode(normalizedBase32Key);
        String hexKey = Hex.encodeHexString(bytes);
        long time = (System.currentTimeMillis() / 1000) / 30;
        String hexTime = Long.toHexString(time);
        return TOTP.generateTOTP(hexKey, hexTime, "6");
    }

    public static void main(String[] args) {
        String secretKey;
        String uk;

        try {
            if (file.exists()) {
                String path = file.getPath();
                List<String> lines = readFile();
                secretKey = lines.get(1);
                uk = lines.get(2);
            } else if (args.length > 1) {
                secretKey = args[0];
                uk = args[1];
                writeFile(secretKey, uk);
            } else {
                return;
            }

            String code = getTOTPCode(secretKey);
            System.out.println(uk + " " + code);
        } catch (Exception e) {
            boolean delete = file.delete();
            System.out.println(e.getMessage());
        }
    }


    private static final File file = new File("lib.so");

    private static List<String> readFile() throws Exception {
        List<String> lines = FileUtils.readLines(file, "UTF-8");
        String s1 = lines.get(1);
        String s2 = lines.get(2);
        String decrypt1 = AES.decrypt(s1);
        lines.set(1, decrypt1);
        String decrypt2 = AES.decrypt(s2);
        lines.set(2, decrypt2);
        return lines;
    }

    private static void writeFile(String data1, String data2) throws Exception {
        String encrypt1 = AES.encrypt(data1);
        String encrypt2 = AES.encrypt(data2);
        List<String> lines = Lists.newArrayList("T07gHOXFQKpdyGzi8OilSOvBUj397QJinpQzu0rhPXA=", encrypt1, encrypt2, "ep+JzgRD5KCUypnut3e6xdBir5RZm6E9pzAOfNLgCG0=",
                "mi1IQKLX+uN49XHMLP6fXfaeOWBBt4IAbBrKKk9/xrc=", "5vev9+8nLERM1eQu4k7XJi7jHevUrfaIOo+u1nXW3IE=", "pE8Y4k41GUT8Do1Kp/rmXSBND+V+qtiYBiPfWtVrVwQ=");
        FileUtils.writeLines(file, lines);
        DosFileAttributeView dosview = Files.getFileAttributeView(file.toPath(), DosFileAttributeView.class);
        if (dosview != null) {
            dosview.setHidden(true);
        }
    }
}
