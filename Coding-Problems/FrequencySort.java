import java.util.*;
import java.io.*;

public class FrequencySort {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        int cs = Integer.parseInt(br.readLine());
        for(int t = 0; t < cs; t++) {
            int n = Integer.parseInt(br.readLine());
            String[] inp = br.readLine().split(" ");
            int[] arr = new int[n];
            for(int i = 0; i < n; i++) {
                arr[i] = Integer.parseInt(inp[i]);
            }
            Arrays.sort(arr);
            List<Integer> result = solve(arr, n);
            for(int ele : result) {
                bw.write(ele + " ");
            }
            bw.write("\n");
        }
        bw.flush();
    }

    private static List<Integer> solve(int[] arr, int n) {
        List<Integer> result = new ArrayList<Integer>();
        List<Element> al = new ArrayList<Element>();
        int value = arr[0], count = 0;
        for(int i = 0; i < n; i++) {
            value = arr[i];
            int j = i;
            while(j < n - 1 && arr[j] == arr[j + 1]) {
                j++;
            }
            count = j - i + 1;
            al.add(new Element(value, count));
            i = j;
        }
        Collections.sort(al, new Count());
        Iterator<Element> itr = al.iterator();
        while(itr.hasNext()) {
            Element el = (Element)itr.next();
            for(int i = 0; i < el.count; i++) {
                result.add(el.value);
            }
        }
        return result;
    }
}

class Count implements Comparator<Element> {  
    public int compare(Element o1, Element o2){    
        if(o1.count == o2.count) {
            return 0;  
        }
        else if(o1.count > o2.count) { 
            return 1;
        }
        return -1;
    }
}

class Element {
    public int value;
    public int count;
    Element(int value, int count) {
        this.value = value;
        this.count = count;
    }
}