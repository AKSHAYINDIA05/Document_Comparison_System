import streamlit as st
import requests
import config as config
import json

def main():
    st.title("Document Comparison System")
    st.write("Upload two documents to compare their content using RAG")

    # Initialize session state for document IDs
    if 'doc1_id' not in st.session_state:
        st.session_state.doc1_id = None
    if 'doc2_id' not in st.session_state:
        st.session_state.doc2_id = None

    # Document upload section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Document 1")
        file1 = st.file_uploader("Upload first document", 
                                type=config.SUPPORTED_FILES,
                                key="file1")
        
        if file1 and not st.session_state.doc1_id:
            with st.spinner("Processing document 1..."):
                files = {"file": file1}
                response = requests.post(f"{config.BACKEND_URL}/upload", files=files)
                
                if response.status_code == 200:
                    st.session_state.doc1_id = response.json()["doc_id"]
                    st.success("Document 1 processed successfully!")
                else:
                    st.error(f"Error processing document 1: {response.text}")

    with col2:
        st.subheader("Document 2")
        file2 = st.file_uploader("Upload second document", 
                                type=config.SUPPORTED_FILES,
                                key="file2")
        
        if file2 and not st.session_state.doc2_id:
            with st.spinner("Processing document 2..."):
                files = {"file": file2}
                response = requests.post(f"{config.BACKEND_URL}/upload", files=files)
                
                if response.status_code == 200:
                    st.session_state.doc2_id = response.json()["doc_id"]
                    st.success("Document 2 processed successfully!")
                else:
                    st.error(f"Error processing document 2: {response.text}")

    # Comparison section
    if st.session_state.doc1_id and st.session_state.doc2_id:
        st.subheader("Document Comparison")
        
        # Optional custom query input
        custom_query = st.text_input(
            "Custom comparison query (optional)",
            placeholder="Enter a specific aspect to compare, or leave blank for general comparison"
        )
        
        if st.button("Compare Documents"):
            with st.spinner("Generating comparison..."):
                response = requests.post(
                    f"{config.BACKEND_URL}/compare",
                    params={
                        "doc1_id": st.session_state.doc1_id,
                        "doc2_id": st.session_state.doc2_id,
                        "query": custom_query if custom_query else None
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display comparison results in tabs
                    tab1, tab2, tab3 = st.tabs(["Comparison", "Document 1 Excerpts", "Document 2 Excerpts"])
                    
                    with tab1:
                        st.markdown("### Comparison Analysis")
                        st.write(result["comparison"])
                    
                    with tab2:
                        st.markdown("### Relevant Excerpts from Document 1")
                        for i, chunk in enumerate(result["doc1_chunks"], 1):
                            st.markdown(f"**Excerpt {i}:**")
                            st.write(chunk)
                            st.divider()
                    
                    with tab3:
                        st.markdown("### Relevant Excerpts from Document 2")
                        for i, chunk in enumerate(result["doc2_chunks"], 1):
                            st.markdown(f"**Excerpt {i}:**")
                            st.write(chunk)
                            st.divider()
                    
                    # Download button for comparison results
                    st.download_button(
                        label="Download Comparison Results",
                        data=json.dumps(result, indent=2),
                        file_name="comparison_results.json",
                        mime="application/json"
                    )
                else:
                    st.error(f"Error generating comparison: {response.text}")

    # Reset button
    if st.button("Reset"):
        st.session_state.doc1_id = None
        st.session_state.doc2_id = None
        st.experimental_rerun()

if __name__ == "__main__":
    main()