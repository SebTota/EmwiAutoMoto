import type {IToken} from "@/interfaces/token";

const LOCAL_STORAGE_NAME_AUTH_TOKEN: string = 'emwi-auto-moto-token';

export const getLocalToken = (): IToken | null => {
    const serializedToken: string | null = localStorage.getItem(LOCAL_STORAGE_NAME_AUTH_TOKEN);
    if (serializedToken) {
        return JSON.parse(serializedToken) as IToken;
    }
    return null;
}

export const saveLocalToken = (token: IToken) => {
    console.log(JSON.stringify(token));
    localStorage.setItem(LOCAL_STORAGE_NAME_AUTH_TOKEN, JSON.stringify(token));
}

export const removeLocalToken = () => {
    localStorage.removeItem(LOCAL_STORAGE_NAME_AUTH_TOKEN);
}
