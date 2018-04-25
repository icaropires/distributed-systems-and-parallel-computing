package matrixClient;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.oxm.jaxb.Jaxb2Marshaller;

@Configuration
public class PairConfiguration {

    @Bean
    public Jaxb2Marshaller marshaller() {
        Jaxb2Marshaller marshaller = new Jaxb2Marshaller();
        // this package must match the package in the <generatePackage> specified in
        // pom.xml
        marshaller.setContextPath("matrixClient.wsdl");
        return marshaller;
    }

    @Bean
    public PairClient pairClient(Jaxb2Marshaller marshaller) {
        PairClient client = new PairClient();
        client.setDefaultUri("http://localhost:8080/ws/pairs.wsdl");
        client.setMarshaller(marshaller);
        client.setUnmarshaller(marshaller);
        return client;
    }

}