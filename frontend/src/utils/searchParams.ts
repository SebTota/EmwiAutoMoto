import type {ISearchParams} from "@/interfaces/searchParams";

const LOCAL_STORAGE_NAME_SEARCH_PARAMS: string = 'emwi-auto-moto-search-params';

export const getSavedSearchParams = (): ISearchParams | null => {
    const serializedToken: string | null = localStorage.getItem(LOCAL_STORAGE_NAME_SEARCH_PARAMS);
    if (serializedToken) {
        return JSON.parse(serializedToken) as ISearchParams;
    }
    return null;
}

export const saveSearchParams = (token: ISearchParams) => {
    localStorage.setItem(LOCAL_STORAGE_NAME_SEARCH_PARAMS, JSON.stringify(token));
}

export const removeSavedSearchParams = () => {
    localStorage.removeItem(LOCAL_STORAGE_NAME_SEARCH_PARAMS);
}

export const savedSearchParamsToRouteParams = () => {
    const savedParams: ISearchParams | null = getSavedSearchParams();
    const queryParams: any = {};

    if (savedParams) {
        if (savedParams.show_sold) queryParams['show_sold'] = savedParams.show_sold;
        if (savedParams.page) queryParams['page'] = savedParams.page;
        if (savedParams.show_status) queryParams['show_status'] = savedParams.show_status;
        if (savedParams.limit) queryParams['limit'] = savedParams.limit;
    }

    return queryParams;
}