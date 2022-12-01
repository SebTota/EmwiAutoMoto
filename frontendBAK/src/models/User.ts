
const LOCAL_STORAGE_NAME_USER: string = 'emwi-auto-moto-user';

export class User {
    id: number;
    first_name: string;
    last_name: string;
    username: string;
    email: string;
    is_active: boolean;
    is_superuser: boolean;

    constructor(id: number, first_name: string, last_name: string, username: string,
                email: string, is_active: boolean, is_superuser: boolean) {
        this.id = id;
        this.first_name = first_name;
        this.last_name = last_name;
        this.username = username;
        this.email = email;
        this.is_active = is_active;
        this.is_superuser = is_superuser;
    }

    private toObject() {
        return {
            "id": this.id,
            "first_name": this.first_name,
            "last_name": this.last_name,
            "username": this.username,
            "email": this.email,
            "is_active": this.is_active,
            "is_superuser": this.is_superuser
        }
    }

    serialize() {
        return JSON.stringify(this.toObject());
    }

    static fromSerialized(serialized: string) {
        const user: ReturnType<User["toObject"]> = JSON.parse(serialized);

        return new User(
          user.id,
          user.first_name,
          user.last_name,
          user.username,
          user.email,
          user.is_active,
          user.is_superuser
        );
    }

}
