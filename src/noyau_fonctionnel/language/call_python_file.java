import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Test {
    public static void main(String[] args) throws IOException, InterruptedException {
        String Script_Path = "./reco_langue.py";
        ProcessBuilder Process_Builder = new
                                         ProcessBuilder("python3",Script_Path)
                                         .inheritIO();

        Process Demo_Process = Process_Builder.start();
        Demo_Process.waitFor();

        BufferedReader Buffered_Reader = new BufferedReader(
                                         new InputStreamReader(
                                         Demo_Process.getInputStream()
                                         ));
        String Output_line = "";

        while ((Output_line = Buffered_Reader.readLine()) != null) {
            System.out.println(Output_line);
        }
    }
}