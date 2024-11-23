import java.util.Arrays;

import src.RSA;

public class Main {
    public static void main(String[] args) {
        RSA rsa = new RSA();
        String fruit = "mango";
        System.out.println(fruit);
        int[] encrypted = rsa.getPublicKey().encrypt(fruit);
        System.out.println(Arrays.toString(encrypted));
        String decrypted = rsa.getPrivateKey().decrypt(encrypted);
        System.out.println(decrypted);
    }
}
