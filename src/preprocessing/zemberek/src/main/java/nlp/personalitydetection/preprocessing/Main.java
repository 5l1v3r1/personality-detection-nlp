package nlp.personalitydetection.preprocessing;

import nlp.personalitydetection.preprocessing.csv.CsvReader;
import nlp.personalitydetection.preprocessing.model.Dataset;

public class Main {
    public static void main(String[] args){
        //TODO: Burası degismeli elemeye ugradıktan sonra olan verisetinden okumalıyız.
        String datasetPath = "/home/khan/Workspace/personality-detection-nlp/data/raw_data/dataset_v2/all_users_v2.csv";
        CsvReader reader = new CsvReader();

        Dataset dataset = reader.readFile(datasetPath, ";");
        System.out.println(dataset.getRows().size());
    }

}