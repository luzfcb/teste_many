# teste_many

### Objetivo de longo prazo:

Substituir o uso do MS Word, e facilitar a analise conteudo do documento por sistemas automatizados.

### Objetivo de curto prazo:

Implementar em `Documento` a capacidade de suportar multiplos `User`'s diferentes possam assinar o mesmo documento e garantir a sua autenticidade



### Glossário:

######`Documento`:

É a representação digital do conteudo de um documento (provavelmente HTML salvo no campo conteudo_documento), e mais algumas informacoes em relacao a ele.


###### `User`:

Usuario do sistema, e possivel assinante de documentos.

###### `Assinatura`:

Representa uma assinatura (hash gerado apartir do conteudo do documento) feita para um determinado documento que está em uma determinada versao

###### `AssinaturaBloco` (vulgo Bloco de assinaturas):

Agregador de assinaturas que estara vinculado a um documento que está em uma determinada versao.
Um documento só poderá possuir um unico bloco de assinatura ativo.
Poderam ocorrer outros blocos de assinatura vinculados a esse documento, mas eles estaram desativados e servirão unicamente para manter o historico de modificacoes.





