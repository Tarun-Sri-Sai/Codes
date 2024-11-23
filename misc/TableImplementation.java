import java.util.*;
import java.io.*;

class Attendance implements Comparator<Table> {
    public int compare(Table o1, Table o2) {
        if (o1.attendance == o2.attendance) {
            return 0;
        } else if (o1.attendance > o2.attendance) {
            return -1;
        }
        return 1;
    }
}

public class TableImplementation {
    public static void main(String[] args) throws IOException {
        Scanner sc = new Scanner(System.in);
        System.out.print("Entries: ");
        int n = sc.nextInt();
        System.out.println();
        List<Table> table = new ArrayList<Table>();
        for (int i = 0; i < n; i++) {
            System.out.println("Entry No #" + (i + 1) + ": ");
            System.out.print("Enter rollno: ");
            int rollno = sc.nextInt();
            System.out.print("Enter name: ");
            String name = sc.next();
            System.out.print("Enter attendance: ");
            float attendance = sc.nextFloat();
            table.add(new Table(rollno, name, attendance));
        }
        System.out.print("1: Sort\n2: Display\n3: Size\nAnything else: Exit\nChoice: ");
        int ch = sc.nextInt();
        System.out.println();
        while (true) {
            switch (ch) {
                case 1:
                    Table.sort(table);
                    break;

                case 2:
                    System.out.print("Size: ");
                    Table.display(table);
                    break;

                case 3:
                    Table.size(table);
                    break;

                default:
                    sc.close();
                    return;
            }
            System.out.print("1: Sort\n2: Display\n3: Size\nAnything else: Exit\nChoice: ");
            ch = sc.nextInt();
            System.out.println();
        }
    }
}

class Table {
    public int rollno;
    public String name = "";
    public float attendance;

    Table(int rollno, String name, float attendance) {
        this.rollno = rollno;
        this.name = name;
        this.attendance = attendance;
    }

    public static void size(List<Table> table) {
        System.out.println(table.size());
    }

    public static void display(List<Table> table) {
        for (Table ele : table) {
            System.out.println(ele.rollno + " | " + ele.name + " | " + ele.attendance);
        }
    }

    public static void sort(List<Table> table) {
        Collections.sort(table, new Attendance());
    }
}