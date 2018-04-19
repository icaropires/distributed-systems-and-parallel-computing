package matrixServer;

import java.util.*;

import io.spring.guides.gs_producing_web_service.Operation;
import org.springframework.stereotype.Component;

@Component
public class PairRepository {
    private static final HashMap<String, LinkedList<Operation>> pairs = new HashMap<>();



    public String insertPair(String key, Operation operation) {
        if(pairs.containsKey(key)) {
            pairs.get(key).add(operation);
        }
        else {
            LinkedList<Operation> operations = new LinkedList<>();
            operations.add(operation);
            pairs.put(key, operations);
        }

        return key;
    }

    public Operation removePair(String key) {
        LinkedList<Operation> operations = pairs.get(key);
        Operation operation = operations.pop();
        if(operations.isEmpty()) {
            pairs.remove(key);
        }

        return operation;
    }
}