# pyrefly: ignore [missing-import]
from sentence_transformers import SentenceTransformer as st
import documents as dc
import numpy as np


class Cosine_similarity:
    model=st('all-MiniLM-L6-v2', local_files_only=True)

    def search(self,query):
        self.doc_emb=Cosine_similarity.model.encode(dc.documents)

        self.query_emb=Cosine_similarity.model.encode(query)

        self.query_norm=np.sqrt(np.sum(self.query_emb**2))

        self.query_normalize=self.query_emb/self.query_norm

        self.query_normalize=np.array([self.query_normalize])

        self.doc_norm=np.sqrt(np.sum(self.doc_emb**2 , axis=1 , keepdims=True))

        self.doc_normalize=(self.doc_emb/self.doc_norm)

        self.query_n_transpose=(self.query_normalize).T

        # print(np.shape(self.doc_normalize),np.shape(self.query_n_transpose))

        self.dot_product=self.doc_normalize@self.query_n_transpose

        self.similarity=np.argsort(-self.dot_product,axis=0).squeeze()

        self.f_dot_product=self.dot_product.squeeze()

        self.doc=np.array(dc.documents)

        self.final=list(zip(self.f_dot_product[self.similarity],self.doc[self.similarity]))

        return np.shape(self.doc_norm)

if __name__=="__main__":
    Cosine_similarity()