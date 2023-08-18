public class Counter {
    public static void main(String[] args) {
        long number = 0;
        for (int i = 0; i < (int) 1e8; i++) {
            number += i;
        }
        System.out.print(number + "\r");
    }
}
