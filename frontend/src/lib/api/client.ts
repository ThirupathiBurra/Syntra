const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export class ApiError extends Error {
  constructor(public status: number, public message: string, public data?: unknown) {
    super(message);
    this.name = "ApiError";
  }
}

export const ApiClient = {
  async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    // Placeholder for auth tokens
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    const config: RequestInit = {
      ...options,
      headers,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        let errorData;
        try {
          errorData = await response.json();
        } catch {
          errorData = { detail: response.statusText };
        }
        throw new ApiError(response.status, errorData.detail || "API Request Failed", errorData);
      }

      // 204 No Content won't have a body
      if (response.status === 204) {
        return {} as T;
      }

      return await response.json() as T;
    } catch (error) {
      if (error instanceof ApiError) throw error;
      throw new ApiError(500, "Network Error", error);
    }
  },

  get<T>(endpoint: string, options?: RequestInit) {
    return this.request<T>(endpoint, { ...options, method: "GET" });
  },

  post<T>(endpoint: string, data: unknown, options?: RequestInit) {
    return this.request<T>(endpoint, {
      ...options,
      method: "POST",
      body: JSON.stringify(data),
    });
  }
};
