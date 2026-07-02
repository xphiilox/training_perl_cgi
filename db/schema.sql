create table if not exists registrations (
    id bigserial primary key,
    name text not null,
    blood_type text not null check (blood_type in ('A', 'B', 'O', 'AB')),
    address text not null,
    created_at timestamptz not null default current_timestamp
);
