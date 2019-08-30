CREATE TABLE public.javlist (
	id serial NOT NULL,
	actor varchar(255) NULL,
	"label" varchar(255) NULL,
	"timestamp" timestamp NULL,
	"path" varchar(255) NULL,
	CONSTRAINT javlist_pk PRIMARY KEY (id)
);
