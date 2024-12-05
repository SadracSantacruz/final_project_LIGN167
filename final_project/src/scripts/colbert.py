import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

class ColBERT:
    def __init__(self, model= "bert-base-uncased"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model = AutoModel.from_pretrained("bert-base-uncased")

    def encode_query(self, query): 
        query_inputs = self.tokenizer(
            query, return_tensors= 'pt', truncation= True, padding= True
        ).to(self.device)

        with torch.no_grad():
            query_embds = self.model(**query_inputs).last_hidden_state

        return query_embds.squeeze(0), query_inputs['attention_mask']

    def encode_documents(self, documents):
        doc_embeddings = []
        doc_attention_masks = []
        for doc in documents:
            doc_inputs = self.tokenizer(
                doc, 
                return_tensors= 'pt',
                truncation= True,
                padding= True
            )

            with torch.no_grad():
                doc_embds = self.model(**doc_inputs).last_hidden_state
            doc_embeddings.append(doc_embds.squeeze(0))
            doc_attention_masks.append(doc_inputs['attention_mask'])

        return doc_embeddings, doc_attention_masks
    
    def rank_documents(self, query, documents, top_k= 5):
        query_embds, query_mask = self.encode_query(query)
        query_embds = F.normalize(query_embds, dim= -1)
        doc_embds, doc_masks = self.encode_documents(documents)

        doc_scores = []
        for doc, doc_embd, doc_mask in zip(documents, doc_embds, doc_masks):
            doc_embd = F.normalize(doc_embd, dim= -1)
            similarity_matrix = torch.matmul(query_embds, doc_embd.transpose(0, 1))
            query_mask = query_mask.bool().squeeze(0) 
            doc_mask = doc_mask.bool().squeeze(0)
            masked_similarities = similarity_matrix
            masked_similarities[~query_mask, :] = float('-inf')
            masked_similarities[:, ~doc_mask] = float('-inf')
            doc_score = torch.max(masked_similarities).item()
            doc_scores.append((doc, doc_score))

        ranked_docs = sorted(doc_scores, key= lambda x: x[1], reverse= True)[:top_k]
        return ranked_docs




    
        

            