const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function queryKnowledgeBase(question){
    const response = await fetch(`${API_BASE_URL}/query`,{
        method: "POST",
        headers: {"Content-Type": "application/json",},
        body: JSON.stringify({question}),
    });

    if(!response.ok){
        throw new Error("Failed to fetch answer");
    }

    return response.json();
}